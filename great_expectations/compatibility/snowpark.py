from __future__ import annotations

import warnings

from great_expectations.compatibility.not_imported import NotImported

SNOWPARK_NOT_IMPORTED = NotImported(
    "snowpark is not installed, please 'pip install snowflake-snowpark-python'"
)

with warnings.catch_warnings():
    # DeprecationWarning: typing.io is deprecated, import directly from typing instead. typing.io will be removed in Python 3.12.
    warnings.simplefilter(action="ignore", category=DeprecationWarning)
    try:
        import snowflake.snowpark
    except ImportError:
        snowpark = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment]

try:
    from snowflake.snowpark import functions
except (ImportError, AttributeError):
    functions = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment]

try:
    from snowflake.snowpark import types
except (ImportError, AttributeError):
    types = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment]

try:
    from snowflake.snowpark  import Session
except ImportError:
    SparkContext = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from pyspark.ml.feature import Bucketizer
except (ImportError, AttributeError):
    Bucketizer = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from snowflake.snowpark import Column
except (ImportError, AttributeError):
    Column = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from snowflake.snowpark import DataFrame
except (ImportError, AttributeError):
    DataFrame = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from snowflake.snowpark import Row
except (ImportError, AttributeError):
    Row = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from snowflake.snowpark import Session
except (ImportError, AttributeError):
    Session = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]


try:
    from snowflake.snowpark import Window
except (ImportError, AttributeError):
    Window = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]

try:
    from snowflake.snowpark.DataFrameReader import DataFrameReader
except (ImportError, AttributeError):
    DataFrameReader = SNOWPARK_NOT_IMPORTED  # type: ignore[assignment,misc]


