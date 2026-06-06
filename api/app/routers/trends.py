"""Price trends endpoint: /trends"""

from __future__ import annotations

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

from ..bigquery import marts_table, query
from ..limiter import limiter

router = APIRouter()


class TrendPoint(BaseModel):
    period_start: str
    period_type: str
    county: str
    region_code: str | None
    sales_count: int
    avg_sold_price_sek: float | None
    avg_price_per_sqm: float | None
    median_sold_price_sek: float | None


@router.get("", response_model=list[TrendPoint])
@limiter.limit("60/minute")
def get_trends(
    request: Request,
    county: str | None = Query(None, description="Filter by county name"),
    period_type: str = Query("month", description="'month' or 'quarter'"),
    limit: int = Query(120, ge=1, le=1000),
) -> list[TrendPoint]:
    where_clauses = [f"period_type = '{period_type}'"]
    if county:
        safe_county = county.replace("'", "''")
        where_clauses.append(f"county = '{safe_county}'")

    where = " AND ".join(where_clauses)
    sql = f"""
        SELECT
            cast(period_start as string) as period_start,
            period_type,
            county,
            region_code,
            sales_count,
            avg_sold_price_sek,
            avg_price_per_sqm,
            median_sold_price_sek
        FROM {marts_table('mart_price_trends')}
        WHERE {where}
        ORDER BY period_start DESC, county
        LIMIT {limit}
    """
    rows = query(sql)
    return [TrendPoint(**r) for r in rows]
