"""Health check endpoint."""

from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..bigquery import get_bq_client

logger = logging.getLogger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    detail: str | None = None


@router.get("/health", response_model=HealthResponse)
def health() -> JSONResponse:
    try:
        client = get_bq_client()
        list(client.query("SELECT 1").result())
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as exc:
        logger.warning("Health check: BigQuery unreachable: %s", exc)
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "detail": "BigQuery unreachable"},
        )
