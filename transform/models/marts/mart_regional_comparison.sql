{{
  config(
    materialized='table',
    description='Cross-county comparison of prices, volumes, and price-per-sqm for the last 12 months.'
  )
}}

with recent_sales as (
    select *
    from {{ ref('fact_sales') }}
    where sold_date >= date_sub(current_date(), interval 12 month)
      and sold_price_sek is not null
),

by_county as (
    select
        county,
        region_code,
        count(*)                                    as total_sales,
        round(avg(sold_price_sek), 0)               as avg_sold_price_sek,
        round(avg(price_per_sqm), 0)                as avg_price_per_sqm,
        round(median(sold_price_sek), 0)            as median_sold_price_sek,
        round(avg(living_area_sqm), 1)              as avg_living_area_sqm,
        round(avg(rooms), 1)                        as avg_rooms,
        countif(object_type = 'lägenhet')           as apartment_count,
        countif(object_type = 'villa')              as villa_count
    from recent_sales
    where county is not null
    group by county, region_code
),

ranked as (
    select
        *,
        rank() over (order by avg_price_per_sqm desc) as price_per_sqm_rank,
        rank() over (order by total_sales desc)        as sales_volume_rank
    from by_county
)

select * from ranked
order by price_per_sqm_rank
