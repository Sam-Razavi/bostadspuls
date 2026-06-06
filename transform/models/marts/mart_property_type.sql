{{
  config(
    materialized='table',
    description='Average price per sqm and sales metrics broken down by county and property type.'
  )
}}

with sales as (
    select
        f.county,
        f.price_per_sqm,
        f.sold_price_sek,
        f.living_area_sqm,
        f.property_type_key
    from {{ ref('fact_sales') }} f
    where f.county is not null
      and f.price_per_sqm is not null
),

joined as (
    select
        s.county,
        dp.object_type,
        dp.object_type_en,
        dp.is_apartment,
        s.price_per_sqm,
        s.sold_price_sek,
        s.living_area_sqm
    from sales s
    join {{ ref('dim_property_type') }} dp
        on s.property_type_key = dp.property_type_key
)

select
    county,
    object_type,
    object_type_en,
    is_apartment,
    count(*)                                as sales_count,
    round(avg(price_per_sqm), 0)            as avg_price_per_sqm,
    round(avg(sold_price_sek), 0)           as avg_sold_price_sek,
    round(avg(living_area_sqm), 1)          as avg_living_area_sqm
from joined
group by 1, 2, 3, 4
order by county, avg_price_per_sqm desc
