"""API endpoint tests using TestClient and a BigQuery mock."""

from __future__ import annotations

from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.routers.regions.query")
def test_regions_endpoint(mock_query):
    mock_query.return_value = [
        {
            "county": "Stockholms län",
            "region_code": "SE-AB",
            "total_sales": 5000,
            "avg_sold_price_sek": 4500000.0,
            "avg_price_per_sqm": 90000.0,
            "median_sold_price_sek": 4200000.0,
            "avg_living_area_sqm": 65.0,
            "price_per_sqm_rank": 1,
            "sales_volume_rank": 1,
        }
    ]
    response = client.get("/regions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["region_code"] == "SE-AB"


@patch("app.routers.regions.query")
def test_region_not_found(mock_query):
    mock_query.return_value = []
    response = client.get("/regions/SE-ZZ")
    assert response.status_code == 404


@patch("app.routers.trends.query")
def test_trends_endpoint(mock_query):
    mock_query.return_value = [
        {
            "period_start": "2024-01-01",
            "period_type": "month",
            "county": "Stockholms län",
            "region_code": "SE-AB",
            "sales_count": 450,
            "avg_sold_price_sek": 4500000.0,
            "avg_price_per_sqm": 90000.0,
            "median_sold_price_sek": 4200000.0,
        }
    ]
    response = client.get("/trends?period_type=month")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["county"] == "Stockholms län"
