"""Unit tests for the Booli ingestion module."""

from __future__ import annotations

import json
import pathlib

import polars as pl
import pytest
from bostadspuls_ingest.booli import _make_checksum, parse_booli_listings

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def booli_data() -> dict:
    return json.loads((FIXTURES / "booli_sold.json").read_text())


def test_make_checksum_deterministic():
    cs1 = _make_checksum("caller123", "secret", 1700000000, "abc123xyz")
    cs2 = _make_checksum("caller123", "secret", 1700000000, "abc123xyz")
    assert cs1 == cs2


def test_make_checksum_format():
    cs = _make_checksum("c", "k", 1, "u")
    assert len(cs) == 40
    assert all(c in "0123456789abcdef" for c in cs)


def test_parse_booli_listings_returns_dataframe(booli_data):
    df = parse_booli_listings(booli_data["sold"])
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 3


def test_parse_booli_listings_columns(booli_data):
    df = parse_booli_listings(booli_data["sold"])
    expected = {"booliId", "soldDate", "soldPrice", "listPrice", "livingArea",
                "rooms", "objectType", "latitude", "longitude", "county", "municipality"}
    assert expected.issubset(set(df.columns))


def test_parse_booli_listings_date_type(booli_data):
    df = parse_booli_listings(booli_data["sold"])
    assert df["soldDate"].dtype == pl.Date


def test_parse_booli_listings_null_list_price(booli_data):
    df = parse_booli_listings(booli_data["sold"])
    nulls = df.filter(pl.col("listPrice").is_null())
    assert len(nulls) == 1
    assert nulls["booliId"][0] == 103


def test_parse_booli_listings_correct_prices(booli_data):
    df = parse_booli_listings(booli_data["sold"])
    row = df.filter(pl.col("booliId") == 101)
    assert row["soldPrice"][0] == 4200000
    assert row["county"][0] == "Stockholms län"


def test_parse_booli_listings_empty():
    df = parse_booli_listings([])
    assert df.is_empty()
