import logging

import pandas as pd
import pyspark.pandas as ps
import pytest
from pyspark import Row
from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql.functions import column

from hamilton import base, driver, htypes, node
from hamilton.experimental import h_spark
from hamilton.log_setup import setup_logging

from .resources import example_module, smoke_screen_module
from .resources.spark import (
    basic_spark_dag,
    pyspark_udfs,
    spark_dag_external_dependencies,
    spark_dag_multiple_with_columns,
    spark_dag_pyspark_udfs,
)

setup_logging(logging.DEBUG)


@pytest.fixture(scope="module")
def spark_session():
    spark = (
        SparkSession.builder.master("local")
        .appName("spark session")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield spark
    spark.stop()


def test_koalas_spark_graph_adapter(spark_session):
    initial_columns = {
        "signups": ps.Series([1, 10, 50, 100, 200, 400], name="signups"),
        "spend": ps.Series([10, 10, 20, 40, 40, 50], name="signups"),
    }
    ps.set_option(
        "compute.ops_on_diff_frames", True
    )  # we should play around here on how to correctly initialize data.
    ps.set_option("compute.default_index_type", "distributed")  # this one doesn't seem to work?
    dr = driver.Driver(
        initial_columns,
        example_module,
        adapter=h_spark.SparkKoalasGraphAdapter(
            spark_session, result_builder=base.PandasDataFrameResult(), spine_column="spend"
        ),
    )
    output_columns = [
        "spend",
        "signups",
        "avg_3wk_spend",
        "spend_per_signup",
    ]
    df = dr.execute(output_columns)
    assert set(df) == set(output_columns)
    expected_column = pd.Series(
        [0.0, 0.0, 13.33333, 23.33333, 33.33333, 43.33333],
        index=[0, 1, 2, 3, 4, 5],
        name="avg_3wk_spend",
    )
    pd.testing.assert_series_equal(
        df.avg_3wk_spend.fillna(0.0).sort_index(), expected_column
    )  # fill na to get around NaN
    # TODO: do some more asserting?


def test_smoke_screen_module(spark_session):
    config = {"region": "US", "pandas_on_spark": True}
    ps.set_option(
        "compute.ops_on_diff_frames", True
    )  # we should play around here on how to correctly initialize data.
    ps.set_option("compute.default_index_type", "distributed")  # this one doesn't seem to work?
    dr = driver.Driver(
        config,
        smoke_screen_module,
        adapter=h_spark.SparkKoalasGraphAdapter(
            spark_session, result_builder=base.PandasDataFrameResult(), spine_column="weeks"
        ),
    )
    output_columns = [
        "raw_acquisition_cost",
        "pessimistic_net_acquisition_cost",
        "neutral_net_acquisition_cost",
        "optimistic_net_acquisition_cost",
        "weeks",
        "series_with_start_date_end_date",
    ]
    df = dr.execute(
        inputs={"date_range": {"start_date": "20200101", "end_date": "20220801"}},
        final_vars=output_columns,
    )
    epsilon = 0.00001
    assert abs(df["raw_acquisition_cost"].mean() - 0.393808) < epsilon
    assert abs(df["pessimistic_net_acquisition_cost"].mean() - 0.420769) < epsilon
    assert abs(df["neutral_net_acquisition_cost"].mean() - 0.405582) < epsilon
    assert abs(df["optimistic_net_acquisition_cost"].mean() - 0.399363) < epsilon
    assert df["series_with_start_date_end_date"].iloc[0] == "date_20200101_date_20220801"


@pytest.mark.parametrize(
    "input_and_expected_fn",
    [
        (lambda df: ({}, (None, {}))),
        (lambda df: ({"a": 1}, (None, {"a": 1}))),
        (lambda df: ({"a": df}, (df, {}))),
        (lambda df: ({"a": df, "b": 1}, (df, {"b": 1}))),
    ],
    ids=["no_kwargs", "one_plain_kwarg", "one_df_kwarg", "one_df_kwarg_and_one_plain_kwarg"],
)
def test__inspect_kwargs(input_and_expected_fn, spark_session):
    """A unit test for inspect_kwargs."""
    pandas_df = pd.DataFrame(
        {"spend": [10, 10, 20, 40, 40, 50], "signups": [1, 10, 50, 100, 200, 400]}
    )
    df = spark_session.createDataFrame(pandas_df)
    input_, expected = input_and_expected_fn(df)
    assert h_spark._inspect_kwargs(input_) == expected


def test__get_pandas_annotations():
    """Unit test for _get_pandas_annotations()."""

    def no_pandas(a: int, b: float) -> float:
        return a * b

    def with_pandas(a: pd.Series) -> pd.Series:
        return a * 2

    def with_pandas_and_other_default(a: pd.Series, b: int) -> pd.Series:
        return a * b

    #
    def with_pandas_and_other_default_with_one_more(a: pd.Series, c: int, b: int = 2) -> pd.Series:
        return a * b * c

    assert h_spark._get_pandas_annotations(node.Node.from_fn(no_pandas), {}) == {
        "a": False,
        "b": False,
    }
    assert h_spark._get_pandas_annotations(node.Node.from_fn(with_pandas), {}) == {"a": True}
    assert h_spark._get_pandas_annotations(
        node.Node.from_fn(with_pandas_and_other_default), {"b": 2}
    ) == {"a": True}
    assert h_spark._get_pandas_annotations(
        node.Node.from_fn(with_pandas_and_other_default_with_one_more), {"b": 2}
    ) == {
        "a": True,
        "c": False,
    }


def test__bind_parameters_to_callable():
    """Unit test for _bind_parameters_to_callable()."""
    actual_kwargs = {"a": 1, "b": 2}
    df_columns = {"b"}
    node_input_types = {"a": (int,), "b": (int,)}
    df_params, params_to_bind = h_spark._determine_parameters_to_bind(
        actual_kwargs, df_columns, node_input_types, "test"
    )
    assert isinstance(df_params["b"], Column)
    assert params_to_bind == {"a": 1}
    assert str(df_params["b"]) == str(column("b"))  # hacky, but compare string representation.


def test__lambda_udf_plain_func(spark_session):
    """Tests plain UDF function"""

    def base_func(a: int, b: int) -> int:
        return a + b

    base_spark_df = spark_session.createDataFrame(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    node_ = node.Node.from_fn(base_func)
    new_df = h_spark._lambda_udf(base_spark_df, node_, {})
    assert new_df.collect() == [Row(a=1, b=4, test=5), Row(a=2, b=5, test=7), Row(a=3, b=6, test=9)]


def test__lambda_udf_pandas_func(spark_session):
    """Tests pandas UDF function"""

    def base_func(a: pd.Series, b: pd.Series) -> htypes.column[pd.Series, int]:
        return a + b

    base_spark_df = spark_session.createDataFrame(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    node_ = node.Node.from_fn(base_func)

    new_df = h_spark._lambda_udf(base_spark_df, node_, {})
    assert new_df.collect() == [Row(a=1, b=4, test=5), Row(a=2, b=5, test=7), Row(a=3, b=6, test=9)]


def test__lambda_udf_pandas_func_error(spark_session):
    """Tests it errors on a bad pandas UDF function"""

    def base_func(a: pd.Series, b: int) -> htypes.column[pd.Series, int]:
        return a + b

    base_spark_df = spark_session.createDataFrame(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    node_ = node.Node.from_fn(base_func)

    with pytest.raises(ValueError):
        h_spark._lambda_udf(base_spark_df, node_, {"a": 1})


def test_smoke_screen_udf_graph_adapter(spark_session):
    """Tests that we can run the PySparkUDFGraphAdapter on a simple graph.

    THe graph has a pandas UDF, a plain UDF that depends on the output of the pandas UDF, and
    also has a parameter bound to it, and then an extra function that isn't satisfied by the
    dataframe, so we add the result as a literal. This should exercise all the code paths
    at least in the result_builder.

    """
    input_df = spark_session.createDataFrame(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    dr = driver.Driver({}, pyspark_udfs, adapter=h_spark.PySparkUDFGraphAdapter())
    inputs = {"a": input_df, "b": input_df, "c": 4, "d": 5}
    output_df = dr.execute(["base_func", "base_func2", "base_func3"], inputs=inputs)
    assert output_df.collect() == [
        Row(a=1, b=4, base_func=5, base_func2=9, base_func3=9),
        Row(a=2, b=5, base_func=7, base_func2=11, base_func3=9),
        Row(a=3, b=6, base_func=9, base_func2=13, base_func3=9),
    ]


def test_base_spark_executor_end_to_end(spark_session):
    # TODO -- make this simpler to call, and not require all these constructs
    dr = (
        driver.Builder()
        .with_modules(basic_spark_dag)
        .with_adapter(base.SimplePythonGraphAdapter(base.DictResult()))
        .build()
    )
    # dr.visualize_execution(
    #     ["processed_df_as_pandas"], "./out", {}, inputs={"spark_session": spark_session}
    # )
    df = dr.execute(["processed_df_as_pandas"], inputs={"spark_session": spark_session})[
        "processed_df_as_pandas"
    ]
    expected_data = {
        "a_times_key": [2, 10, 24, 44, 70],
        "b_times_key": [5, 16, 33, 56, 85],
        "a_plus_b_plus_c": [10.5, 20.0, 29.5, 39.0, 48.5],
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(df, expected_df, check_names=False, check_dtype=False)


def test_base_spark_executor_end_to_end_external_dependencies(spark_session):
    # TODO -- make this simpler to call, and not require all these constructs
    dr = (
        driver.Builder()
        .with_modules(spark_dag_external_dependencies)
        .with_adapter(base.SimplePythonGraphAdapter(base.DictResult()))
        .build()
    )
    dfs = dr.execute(
        ["processed_df_as_pandas", "processed_df_as_pandas_with_external_inputs"],
        inputs={"spark_session": spark_session},
    )

    expected_df = pd.DataFrame({"a": [2, 3, 4, 5], "b": [4, 6, 8, 10]})
    processed_df_as_pandas = pd.DataFrame(dfs["processed_df_as_pandas"])
    pd.testing.assert_frame_equal(
        processed_df_as_pandas, expected_df, check_names=False, check_dtype=False
    )

    processed_df_as_pandas_with_external_inputs = pd.DataFrame(
        dfs["processed_df_as_pandas_with_external_inputs"]
    )
    pd.testing.assert_frame_equal(
        processed_df_as_pandas,
        processed_df_as_pandas_with_external_inputs,
        check_names=False,
        check_dtype=False,
    )


def test_base_spark_executor_end_to_end_multiple_with_columns(spark_session):
    dr = (
        driver.Builder()
        .with_modules(spark_dag_multiple_with_columns)
        .with_adapter(base.SimplePythonGraphAdapter(base.DictResult()))
        .build()
    )
    df = dr.execute(["final"], inputs={"spark_session": spark_session})["final"].sort_index(axis=1)

    expected_df = pd.DataFrame(
        {
            "d_raw": [1, 4, 7, 10],
            "e_raw": [2, 5, 8, 11],
            "f_raw": [5, 10, 15, 20],
            "d": [6, 9, 12, 15],
            "f": [17.5, 35.0, 52.5, 70.0],
            "e": [12.3, 18.299999, 24.299999, 30.299999],
            "multiply_d_e_f_key": [1291.5, 11529.0, 45927.0, 127260.0],
            "key": [1, 2, 3, 4],
            "a_times_key": [2, 10, 24, 44],
            "b_times_key": [5, 16, 33, 56],
            "a_plus_b_plus_c": [10.5, 20.0, 29.5, 39.0],
        }
    ).sort_index(axis=1)
    pd.testing.assert_frame_equal(df, expected_df, check_names=False, check_dtype=False)


def _no_pyspark_dataframe_parameter(foo: int) -> int:
    ...


def _one_pyspark_dataframe_parameter(foo: DataFrame, bar: int) -> DataFrame:
    ...


def _two_pyspark_dataframe_parameters(foo: DataFrame, bar: int, baz: DataFrame) -> DataFrame:
    ...


@pytest.mark.parametrize(
    "fn,requested_parameter,expected",
    [
        (_one_pyspark_dataframe_parameter, "foo", "foo"),
        (_one_pyspark_dataframe_parameter, None, "foo"),
        (_two_pyspark_dataframe_parameters, "foo", "foo"),
        (_two_pyspark_dataframe_parameters, "baz", "baz"),
    ],
)
def test_derive_dataframe_parameter_succeeds(fn, requested_parameter, expected):
    assert h_spark.derive_dataframe_parameter_from_fn(fn, requested_parameter) == expected
    n = node.Node.from_fn(fn)
    assert h_spark.derive_dataframe_parameter_from_node(n, requested_parameter) == expected


@pytest.mark.parametrize(
    "fn,requested_parameter",
    [
        (_no_pyspark_dataframe_parameter, "foo"),
        (_no_pyspark_dataframe_parameter, None),
        (_one_pyspark_dataframe_parameter, "baz"),
        (_two_pyspark_dataframe_parameters, "bar"),
        (_two_pyspark_dataframe_parameters, None),
    ],
)
def test_derive_dataframe_parameter_fails(fn, requested_parameter):
    with pytest.raises(ValueError):
        h_spark.derive_dataframe_parameter_from_fn(fn, requested_parameter)
        n = node.Node.from_fn(fn)
        h_spark.derive_dataframe_parameter_from_node(n, requested_parameter)


def test_prune_nodes_no_select():
    nodes = [
        node.Node.from_fn(fn) for fn in [basic_spark_dag.a, basic_spark_dag.b, basic_spark_dag.c]
    ]
    select = None
    assert {n for n in h_spark.prune_nodes(nodes, select)} == set(nodes)


def test_prune_nodes_single_select():
    nodes = [
        node.Node.from_fn(fn) for fn in [basic_spark_dag.a, basic_spark_dag.b, basic_spark_dag.c]
    ]
    select = ["a", "b"]
    assert {n for n in h_spark.prune_nodes(nodes, select)} == set(nodes[0:2])


def test_generate_nodes_invalid_select():
    dec = h_spark.with_columns(
        basic_spark_dag.a,
        basic_spark_dag.b,
        basic_spark_dag.c,
        select=["d"],  # not a node
        initial_schema=["a_raw", "b_raw", "c_raw", "key"],
    )
    with pytest.raises(ValueError):

        def df_as_pandas(df: DataFrame) -> pd.DataFrame:
            return df.toPandas()

        dec.generate_nodes(df_as_pandas, {})


def test_with_columns_generate_nodes_no_select():
    dec = h_spark.with_columns(
        basic_spark_dag.a,
        basic_spark_dag.b,
        basic_spark_dag.c,
        initial_schema=["a_raw", "b_raw", "c_raw", "key"],
    )

    def df_as_pandas(df: DataFrame) -> pd.DataFrame:
        return df.toPandas()

    nodes = dec.generate_nodes(df_as_pandas, {})
    nodes_by_names = {n.name: n for n in nodes}
    assert set(nodes_by_names.keys()) == {
        "df_as_pandas.a",
        "df_as_pandas.b",
        "df_as_pandas.c",
        "df_as_pandas",
    }


def test_with_columns_generate_nodes_select():
    dec = h_spark.with_columns(
        basic_spark_dag.a,
        basic_spark_dag.b,
        basic_spark_dag.c,
        initial_schema=["a_raw", "b_raw", "c_raw", "key"],
        select=["c"],
    )

    def df_as_pandas(df: DataFrame) -> pd.DataFrame:
        return df.toPandas()

    nodes = dec.generate_nodes(df_as_pandas, {})
    nodes_by_names = {n.name: n for n in nodes}
    assert set(nodes_by_names.keys()) == {"df_as_pandas.c", "df_as_pandas"}


def test_with_columns_generate_nodes_specify_namespace():
    dec = h_spark.with_columns(
        basic_spark_dag.a,
        basic_spark_dag.b,
        basic_spark_dag.c,
        initial_schema=["a_raw", "b_raw", "c_raw", "key"],
        namespace="foo",
    )

    def df_as_pandas(df: DataFrame) -> pd.DataFrame:
        return df.toPandas()

    nodes = dec.generate_nodes(df_as_pandas, {})
    nodes_by_names = {n.name: n for n in nodes}
    assert set(nodes_by_names.keys()) == {"foo.a", "foo.b", "foo.c", "df_as_pandas"}


def test__format_pandas_udf():
    assert (
        h_spark._format_pandas_udf("foo", ["a", "b"]).strip()
        == "def foo(a: pd.Series, b: pd.Series) -> pd.Series:\n"
        "    return partial_fn(a=a, b=b)"
    )


def test__format_standard_udf():
    assert (
        h_spark._format_udf("foo", ["b", "a"]).strip() == "def foo(b, a):\n"
        "    return partial_fn(b=b, a=a)"
    )


def test_sparkify_node():
    def foo(
        a_from_upstream: pd.Series, b_from_upstream: pd.Series, c_from_df: pd.Series, d_fixed: int
    ) -> htypes.column[pd.Series, int]:
        return a_from_upstream + b_from_upstream + c_from_df + d_fixed

    node_ = node.Node.from_fn(foo)
    sparkified = h_spark.sparkify_node(
        node_,
        "df_upstream",
        "df_base",
        {"a_from_upstream", "b_from_upstream"},
        {"c_from_df"},
    )
    # Superset of all the original nodes except the ones from the dataframe
    # (as we already have that) both the physical and the logical dependencies
    assert set(sparkified.input_types) == {
        "a_from_upstream",
        "b_from_upstream",
        "d_fixed",
        "df_base",
        "df_upstream",
    }


def test_pyspark_udfs_end_to_end(spark_session):
    # TODO -- make this simpler to call, and not require all these constructs
    dr = (
        driver.Builder()
        .with_modules(spark_dag_pyspark_udfs)
        .with_adapter(base.SimplePythonGraphAdapter(base.DictResult()))
        .build()
    )
    # dr.visualize_execution(
    #     ["processed_df_as_pandas"], "./out", {}, inputs={"spark_session": spark_session}
    # )
    df = dr.execute(["processed_df_as_pandas"], inputs={"spark_session": spark_session})[
        "processed_df_as_pandas"
    ]
    expected_data = {
        "a_times_key": [2, 10, 24, 44, 70],
        "b_times_key": [5, 16, 33, 56, 85],
        "a_plus_b_plus_c": [10.5, 20.0, 29.5, 39.0, 48.5],
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(df, expected_df, check_names=False, check_dtype=False)


# is default
def pyspark_fn_1(foo: DataFrame) -> DataFrame:
    pass


# is default
def pyspark_fn_2(foo: DataFrame, bar: int) -> DataFrame:
    pass


def not_pyspark_fn(foo: DataFrame, bar: DataFrame) -> DataFrame:
    pass


@pytest.mark.parametrize(
    "fn,expected", [(pyspark_fn_1, True), (pyspark_fn_2, True), (not_pyspark_fn, False)]
)
def test_is_default_pyspark_node(fn, expected):
    node_ = node.Node.from_fn(fn)
    assert h_spark.transforms.is_default_pyspark_udf(node_) == expected
