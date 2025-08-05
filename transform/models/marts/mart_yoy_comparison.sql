{{
  config(
    materialized='table',
    description='Year-over-year price change per county and period. Self-joins mart_price_trends offset by 12 months.'
  )
}}

with trends as (
    select * from {{ ref('mart_price_trends') }}
    where avg_price_per_sqm is not null
)

select
    c.county,
    c.region_code,
    c.period_start,
    c.period_type,
    c.sales_count,
    c.avg_price_per_sqm,
    p.avg_price_per_sqm                                         as prior_year_avg_price_per_sqm,
    round(
        (c.avg_price_per_sqm - p.avg_price_per_sqm)
        / nullif(p.avg_price_per_sqm, 0) * 100,
        2
    )                                                           as yoy_pct_change
from trends c
left join trends p
    on  c.county      = p.county
    and c.period_type = p.period_type
    and c.period_start = date_add(p.period_start, interval 1 year)
order by c.county, c.period_start desc
