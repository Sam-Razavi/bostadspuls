{{
  config(
    materialized='table',
    description='Fact table: one row per sold property. Grain = booli_id.'
  )
}}

with listings as (
    select * from {{ ref('stg_booli__listings') }}
),

dim_loc as (
    select * from {{ ref('dim_location') }}
),

dim_prop as (
    select * from {{ ref('dim_property_type') }}
),

joined as (
    select
        l.booli_id,
        l.sold_date,
        l.sold_price_sek,
        l.list_price_sek,
        l.living_area_sqm,
        l.rooms,
        l.price_per_sqm,
        l.price_vs_list_pct,
        l.latitude,
        l.longitude,
        l.street_address,

        -- Dimension foreign keys
        dl.location_key,
        dp.property_type_key,

        -- Degenerate dimensions
        l.county,
        l.municipality,
        l.city,
        l.object_type

    from listings l
    left join dim_loc dl
        on l.county = dl.county
        and coalesce(l.municipality, '') = coalesce(dl.municipality, '')
        and coalesce(l.city, '') = coalesce(dl.city, '')
    left join dim_prop dp
        on l.object_type = dp.object_type
)

select * from joined
