"""Property type breakdown endpoint: /property-types"""

from __future__ import annotations

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

from ..bigquery import marts_table, query
from ..limiter import limiter

router = APIRouter()


class PropertyTypeSummary(BaseModel):
    county: str
    object_type: str
    object_type_en: str
    is_apartment: bool
    sales_count: int
    avg_price_per_sqm: float | None
    avg_sold_price_sek: float | None
    avg_living_area_sqm: float | None


@router.get("", response_model=list[PropertyTypeSummary])
@limiter.limit("60/minute")
def get_property_types(
    request: Request,
    county: str | None = Query(None, description="Filter by county name"),
) -> list[PropertyTypeSummary]:
    where = ""
    if county:
        safe_county = county.replace("'", "''")
        where = f"WHERE county = '{safe_county}'"

    sql = f"""
        SELECT
            county,
            object_type,
            object_type_en,
            is_apartment,
            sales_count,
            avg_price_per_sqm,
            avg_sold_price_sek,
            avg_living_area_sqm
        FROM {marts_table('mart_property_type')}
        {where}
        ORDER BY county, avg_price_per_sqm DESC
    """
    rows = query(sql)
    return [PropertyTypeSummary(**r) for r in rows]
