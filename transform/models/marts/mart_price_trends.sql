{{
  config(
    materialized='table',
    description='Monthly and quarterly price trend aggregations per region.'
  )
}}

with fact as (
    select
        f.sold_date,
        f.sold_price_sek,
        f.price_per_sqm,
        f.county,
        -- Derive region_code from county via dim_location join
        dl.region_code
    from {{ ref('fact_sales') }} f
    left join {{ ref('dim_location') }} dl
        on f.location_key = dl.location_key
    where f.sold_price_sek is not null
),

monthly as (
    select
        date_trunc(sold_date, month)                        as period_start,
        'month'                                             as period_type,
        county,
        region_code,
        count(*)                                            as sales_count,
        round(avg(sold_price_sek), 0)                       as avg_sold_price_sek,
        round(avg(price_per_sqm), 0)                        as avg_price_per_sqm,
        round(median(sold_price_sek), 0)                    as median_sold_price_sek,
        min(sold_price_sek)                                 as min_sold_price_sek,
        max(sold_price_sek)                                 as max_sold_price_sek
    from fact
    group by 1, 2, 3, 4
),

quarterly as (
    select
        date_trunc(sold_date, quarter)                      as period_start,
        'quarter'                                           as period_type,
        county,
        region_code,
        count(*)                                            as sales_count,
        round(avg(sold_price_sek), 0)                       as avg_sold_price_sek,
        round(avg(price_per_sqm), 0)                        as avg_price_per_sqm,
        round(median(sold_price_sek), 0)                    as median_sold_price_sek,
        min(sold_price_sek)                                 as min_sold_price_sek,
        max(sold_price_sek)                                 as max_sold_price_sek
    from fact
    group by 1, 2, 3, 4
)

select * from monthly
union all
select * from quarterly
