from typing import List

import attrs
import pypika
from pypika import terms

from tecton_core import time_utils
from tecton_core.query import nodes
from tecton_core.query import sql_compat
from tecton_core.query_consts import ANCHOR_TIME
from tecton_proto.common import aggregation_function_pb2 as afpb
from tecton_proto.data import feature_view_pb2
from tecton_snowflake.query import aggregation_plans
from tecton_snowflake.query import queries


@attrs.frozen
class PartialAggSnowflakeNode(nodes.PartialAggNode):
    """
    Using a different implementation for LastN/FirstN aggregation functions for Snowflake
    """

    @classmethod
    def from_query_node(cls, query_node: nodes.PartialAggNode) -> "PartialAggSnowflakeNode":
        return cls(
            input_node=query_node.input_node,
            fdw=query_node.fdw,
            window_start_column_name=query_node.window_start_column_name,
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
        )

    def _get_partial_agg_columns(self) -> List[terms.Term]:
        """
        Override PartialAggNode's _get_partial_agg_columns to use the Snowflake implementation
        """
        time_aggregation = self.fdw.trailing_time_window_aggregation
        agg_cols = []
        output_columns = set()
        for feature in time_aggregation.features:
            aggregation_plan = aggregation_plans.get_aggregation_plan(
                feature.function, feature.function_params, self.fdw.time_key
            )
            agg_query_terms = aggregation_plan.partial_aggregation_query_terms(feature.input_feature_name)
            materialized_column_names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            assert len(agg_query_terms) == len(materialized_column_names)
            for column_name, aggregated_column in zip(
                materialized_column_names,
                agg_query_terms,
            ):
                if column_name in output_columns:
                    continue
                output_columns.add(column_name)
                agg_cols.append(aggregated_column.as_(column_name))
        return agg_cols


@attrs.frozen
class AsofJoinFullAggSnowflakeNode(nodes.AsofJoinFullAggNode):
    """
    Asof join full agg rollup, using band joins
    """

    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinFullAggNode):
        return cls(**attrs.asdict(query_node, recurse=False))

    def _to_query(self) -> pypika.Query:
        """
        Snowflake doesn't support RANGE BETWEEN with sliding window as of 07/27/2023, they have it on the roadmap but no ETA.
        This implmentation treat every feature in an aggregation as a separate query, and then join them together.

        :return: Query
        """
        time_aggregation = self.fdw.trailing_time_window_aggregation
        join_keys = list(self.spine.node.columns)

        # Generate sub queries for each feature
        sub_queries = []
        for feature in time_aggregation.features:
            sub_query = self._to_single_feature_aggregate_query(feature)
            sub_queries.append(sub_query)

        # Join all sub queries together
        result_df = sub_queries[0]
        for query in sub_queries[1:]:
            left_q = result_df
            right_q = query
            join_q = queries.SnowflakeQuery().from_(left_q)
            join_q = join_q.inner_join(right_q)
            result_df = join_q.using(*join_keys).select("*")
        return result_df

    def _to_single_feature_aggregate_query(self, aggregate_feature: feature_view_pb2.AggregateFeature) -> pypika.Query:
        """
        Helper method to run one aggregate feature. This does not use the Range Between implemention.

        :param aggregate_feature: AggregateFeature data proto
        :return: Query
        """
        left_df = self.spine.node._to_query()
        right_df = self.partial_agg_node.node._to_query()
        join_keys = self.fdw.join_keys
        # When calling ghf() with time range, spine only has _ANCHOR_TIME but not time_key
        timestamp_join_cols = [self.fdw.time_key] if self.fdw.time_key in join_keys else [ANCHOR_TIME]
        common_cols = join_keys + timestamp_join_cols

        output_columns = list(self.spine.node.columns)

        left_name = self.spine.node.__class__.__name__ + "_" + str(id(self.spine.node))

        agg_name = self.partial_agg_node.node.__class__.__name__ + "_" + str(id(self.partial_agg_node.node))

        output_feature_name = sql_compat.default_case(aggregate_feature.output_feature_name)
        window = time_utils.convert_proto_duration_for_version(
            aggregate_feature.window, self.fdw.get_feature_store_format_version
        )
        aggregation_plan = aggregation_plans.get_aggregation_plan(
            aggregate_feature.function,
            aggregate_feature.function_params,
            f"{agg_name}.{ANCHOR_TIME}",
        )
        names = aggregation_plan.materialized_column_names(aggregate_feature.input_feature_name)
        agg_columns = [*common_cols, aggregation_plan.full_aggregation_join_query_term(names).as_(output_feature_name)]
        # Join spine and partial agg node
        agg_from = (
            queries.SnowflakeQuery()
            .from_(pypika.AliasedQuery(left_name))
            .inner_join(pypika.AliasedQuery(agg_name))
            .on_field(*join_keys)
        )
        # Flatten the input feature if the aggregation function is last/first non-distinct N
        if aggregate_feature.function in {
            afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
            afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
        }:
            agg_from = agg_from.lateral(pypika.Field(f"FLATTEN(input=>{names[0]})"))
        # Add the condition that spine time is between partial agg time and partial agg time + window, and run the aggregation function
        agg = (
            agg_from.select(*agg_columns)
            .where(pypika.AliasedQuery(left_name)._ANCHOR_TIME >= pypika.AliasedQuery(agg_name)._ANCHOR_TIME)
            .where(pypika.AliasedQuery(left_name)._ANCHOR_TIME < pypika.AliasedQuery(agg_name)._ANCHOR_TIME + window)
            .groupby(*(pypika.AliasedQuery(left_name).field(column) for column in common_cols))
        )

        output_feature_name = sql_compat.default_case(aggregate_feature.output_feature_name)
        spine_name = left_name + "_" + output_feature_name
        right_name = agg_name + "_AGG"
        feature_column = pypika.AliasedQuery(right_name).field(output_feature_name)
        # TODO(TEC-15924): This behavior is not the same as spark. We should consider consolidating this behavior.
        if aggregate_feature.function == afpb.AggregationFunction.AGGREGATION_FUNCTION_COUNT:
            feature_column = queries.ZeroIfNull(feature_column).as_(output_feature_name)
        # Join the result with the spine node
        join_df = (
            queries.SnowflakeQuery()
            .with_(left_df, spine_name)
            .with_(agg, right_name)
            .from_(pypika.AliasedQuery(spine_name))
            .left_join(pypika.AliasedQuery(right_name))
            .on_field(*common_cols)
            .select(*output_columns, feature_column)
        )
        output_columns.append(output_feature_name)

        return (
            queries.SnowflakeQuery()
            .with_(left_df, left_name)
            .with_(right_df, agg_name)
            .from_(join_df)
            .select(*output_columns)
        )
