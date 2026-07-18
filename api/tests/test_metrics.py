from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_metrics_endpoint_returns_prometheus_text():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text
