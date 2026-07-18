"""Tests for the /compare (year-over-year) endpoint."""

from __future__ import annotations

from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

_MOCK_ROW = {
    "county": "Stockholms län",
    "region_code": "SE-AB",
    "period_start": "2024-01-01",
    "period_type": "month",
    "sales_count": 450,
    "avg_price_per_sqm": 92000.0,
    "prior_year_avg_price_per_sqm": 88000.0,
    "yoy_pct_change": 4.55,
}


@patch("app.routers.compare.query")
def test_compare_returns_list(mock_query):
    mock_query.return_value = [_MOCK_ROW]
    response = client.get("/compare")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["yoy_pct_change"] == 4.55


@patch("app.routers.compare.query")
def test_compare_null_yoy(mock_query):
    row = {**_MOCK_ROW, "prior_year_avg_price_per_sqm": None, "yoy_pct_change": None}
    mock_query.return_value = [row]
    response = client.get("/compare")
    assert response.status_code == 200
    assert response.json()[0]["yoy_pct_change"] is None


@patch("app.routers.compare.query")
def test_compare_period_type_filter(mock_query):
    mock_query.return_value = [_MOCK_ROW]
    response = client.get("/compare?period_type=quarter")
    assert response.status_code == 200
    sql_used = mock_query.call_args[0][0]
    assert "quarter" in sql_used
