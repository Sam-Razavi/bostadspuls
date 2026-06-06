"""Unit tests for the SCB ingestion module."""

from __future__ import annotations

import json
import pathlib

import polars as pl
import pytest

from bostadspuls_ingest.scb import parse_price_index, parse_sales_volume, parse_scb_response
from bostadspuls_ingest.regions import add_region_code, add_county_name, COUNTY_CODE_MAP

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def price_index_data() -> dict:
    return json.loads((FIXTURES / "scb_price_index.json").read_text())


def test_parse_scb_response_returns_dataframe(price_index_data):
    df = parse_scb_response(price_index_data)
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 6


def test_parse_scb_response_null_on_missing_value(price_index_data):
    df = parse_scb_response(price_index_data)
    val_col = [c for c in df.columns if c not in ("Region", "Tid", "region_code")][0]
    nulls = df.filter(pl.col(val_col).is_null())
    assert len(nulls) == 1


def test_parse_price_index_typed_columns(price_index_data):
    df = parse_price_index(price_index_data)
    assert "price_index" in df.columns
    assert df["price_index"].dtype == pl.Float64
    assert "quarter" in df.columns
    assert "region_code" in df.columns


def test_parse_price_index_region_codes(price_index_data):
    df = parse_price_index(price_index_data)
    stockholm_rows = df.filter(pl.col("Region") == "0180")
    assert all(rc == "SE-AB" for rc in stockholm_rows["region_code"].to_list() if rc is not None)


def test_normalize_region_codes_unknown_prefix():
    df = pl.DataFrame({"Region": ["9999", "0180"]})
    result = add_region_code(df)
    assert result["region_code"][0] is None
    assert result["region_code"][1] == "SE-AB"


def test_add_county_name():
    df = pl.DataFrame({"region_code": ["SE-AB", "SE-M", "SE-BD"]})
    result = add_county_name(df)
    assert "county_name" in result.columns
    assert result["county_name"][0] == "Stockholms län"
    assert result["county_name"][2] == "Norrbottens län"


def test_county_code_map_complete():
    assert len(COUNTY_CODE_MAP) == 21


def test_parse_scb_response_region_dtype(price_index_data):
    """Region column must be String even when values look numeric (e.g. '0180')."""
    df = parse_scb_response(price_index_data)
    assert df["Region"].dtype == pl.String


def test_parse_price_index_empty_data():
    df = parse_price_index({"columns": [], "data": []})
    assert df.is_empty()
