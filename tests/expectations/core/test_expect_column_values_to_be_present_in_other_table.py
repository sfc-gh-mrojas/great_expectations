from typing import Final

import pandas as pd
import pytest
from contrib.experimental.great_expectations_experimental.expectations.expect_column_values_to_be_present_in_other_table import (
    ExpectColumnValuesToBePresentInAnotherTable,  # needed for expectation registration
)

from great_expectations.compatibility.sqlalchemy_compatibility_wrappers import (
    add_dataframe_to_db,
)
from great_expectations.data_context.util import file_relative_path
from great_expectations.datasource.fluent import SqliteDatasource

DB_PATH: Final[str] = file_relative_path(
    __file__, "../../test_sets/referential_integrity_dataset.db"
)


@pytest.fixture
def referential_integrity_db(sa):
    sqlite_engine = sa.create_engine(f"sqlite:///{DB_PATH}")
    order_table_1 = pd.DataFrame(
        {
            "ORDER_ID": ["aaa", "bbb", "ccc"],
            "CUSTOMER_ID": [1, 1, 3],
        }
    )
    order_table_2 = pd.DataFrame(
        {
            "ORDER_ID": ["aaa", "bbb", "ccc"],
            "CUSTOMER_ID": [1, 5, 6],
        }
    )
    customer_table = pd.DataFrame(
        {
            "CUSTOMER_ID": [1, 2, 3],
        }
    )

    add_dataframe_to_db(
        df=order_table_1,
        name="order_table_1",
        con=sqlite_engine,
        index=False,
        if_exists="replace",
    )
    add_dataframe_to_db(
        df=order_table_2,
        name="order_table_2",
        con=sqlite_engine,
        index=False,
        if_exists="replace",
    )
    add_dataframe_to_db(
        df=customer_table,
        name="customer_table",
        con=sqlite_engine,
        index=False,
        if_exists="replace",
    )
    return sqlite_engine


@pytest.fixture()
def sqlite_datasource(
    in_memory_runtime_context, referential_integrity_db
) -> SqliteDatasource:
    context = in_memory_runtime_context
    datasource_name = "my_snowflake_datasource"
    return context.sources.add_sqlite(
        datasource_name, connection_string=f"sqlite:///{DB_PATH}"
    )


@pytest.mark.sqlite
def test_successful_expectation_run(sqlite_datasource):
    datasource = sqlite_datasource
    asset_name = "order_table_1"
    asset = datasource.add_table_asset(name=asset_name, table_name="order_table_1")
    batch = asset.get_batch_list_from_batch_request(asset.build_batch_request())[0]
    res = batch.validate(
        ExpectColumnValuesToBePresentInAnotherTable(
            foreign_key_column="CUSTOMER_ID",
            foreign_table="customer_table",
            foreign_table_key_column="CUSTOMER_ID",
        )
    )
    assert res.success is True


@pytest.mark.sqlite
def test_failed_expectation_run(sqlite_datasource):
    datasource = sqlite_datasource
    asset_name = "order_table_2"
    asset = datasource.add_table_asset(name=asset_name, table_name="order_table_2")
    batch = asset.get_batch_list_from_batch_request(asset.build_batch_request())[0]
    res = batch.validate(
        ExpectColumnValuesToBePresentInAnotherTable(
            foreign_key_column="CUSTOMER_ID",
            foreign_table="customer_table",
            foreign_table_key_column="CUSTOMER_ID",
        )
    )
    assert res.success is False
    assert res["result"]["observed_value"] == "2 missing values."
    assert res["result"]["unexpected_index_list"] == [
        {"CUSTOMER_ID": 5},
        {"CUSTOMER_ID": 6},
    ]


@pytest.mark.sqlite
def test_configuration_invalid_column_name(sqlite_datasource):
    """What does this test do, and why?

    This is testing default behavior of `batch.validate()` which catches Exception information
    and places it in `exception_info`. Here we check that the exception message contains the text we expect
    """
    datasource = sqlite_datasource
    asset_name = "order_table_2"
    asset = datasource.add_table_asset(name=asset_name, table_name="order_table_2")
    batch = asset.get_batch_list_from_batch_request(asset.build_batch_request())[0]
    res = batch.validate(
        ExpectColumnValuesToBePresentInAnotherTable(
            foreign_key_column="I_DONT_EXIST",
            foreign_table="customer_table",
            foreign_table_key_column="CUSTOMER_ID",
        ),
    )

    assert res.success is False
    assert res["exception_info"]["raised_exception"] is True
    assert (
        "no such column: a.I_DONT_EXIST" in res["exception_info"]["exception_message"]
    )


@pytest.mark.unit
def test_template_dict_creation():
    expectation = ExpectColumnValuesToBePresentInAnotherTable(
        foreign_key_column="CUSTOMER_ID",
        foreign_table="customer_table",
        foreign_table_key_column="CUSTOMER_ID",
    )
    assert expectation.template_dict == {
        "foreign_key_column": "CUSTOMER_ID",
        "foreign_table": "customer_table",
        "foreign_table_key_column": "CUSTOMER_ID",
    }
