from enum import Enum


class QueryTreeComputeType(Enum):
    # Compute responsible for generating un-aggregated results of a FV pipeline
    STAGING = 1
    # Compute responsible for running partial + full aggregations & the as-of join
    AGGREGATION = 2
    ODFV = 3


class QueryTreeOutputType(Enum):
    PANDAS = 1
    # Note: below two are not used yet, but should be implemented
    SPARK = 2
    S3 = 3


# Where to stage results to when using the query tree executor.
# By default, this will stage to memory (i.e. Snowflake -> memory -> DuckDB)
class QueryTreeStagingLocation(Enum):
    DWH = 1
    S3 = 2
    MEMORY = 3
