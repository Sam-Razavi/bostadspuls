"""Tests for the /property-types endpoint."""

from __future__ import annotations

from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

_MOCK_ROW = {
    "county": "Stockholms län",
    "object_type": "lägenhet",
    "object_type_en": "Apartment",
    "is_apartment": True,
    "sales_count": 3200,
    "avg_price_per_sqm": 92000.0,
    "avg_sold_price_sek": 4600000.0,
    "avg_living_area_sqm": 58.5,
}


@patch("app.routers.property_types.query")
def test_property_types_returns_list(mock_query):
    mock_query.return_value = [_MOCK_ROW]
    response = client.get("/property-types")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["object_type_en"] == "Apartment"
    assert data[0]["is_apartment"] is True


@patch("app.routers.property_types.query")
def test_property_types_county_filter(mock_query):
    mock_query.return_value = [_MOCK_ROW]
    response = client.get("/property-types?county=Stockholms+l%C3%A4n")
    assert response.status_code == 200
    assert mock_query.called
    sql_used = mock_query.call_args[0][0]
    assert "Stockholms l" in sql_used


@patch("app.routers.property_types.query")
def test_property_types_empty(mock_query):
    mock_query.return_value = []
    response = client.get("/property-types")
    assert response.status_code == 200
    assert response.json() == []
