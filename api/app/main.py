"""FastAPI application entry point."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .logging_config import configure_logging
from .routers import compare, health, property_types, regions, trends

configure_logging()
logger = logging.getLogger(__name__)

_raw_origins = settings.cors_origins.strip()
CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()] or ["*"]

app = FastAPI(
    title="Bostadspuls API",
    description="Swedish housing market analytics API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(health.router)
app.include_router(trends.router, prefix="/trends", tags=["trends"])
app.include_router(regions.router, prefix="/regions", tags=["regions"])
app.include_router(property_types.router, prefix="/property-types", tags=["property-types"])
app.include_router(compare.router, prefix="/compare", tags=["compare"])
