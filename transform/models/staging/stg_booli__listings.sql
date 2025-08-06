{{
  config(
    materialized='view',
    description='Staged Booli sold listings: renamed, cast, price-per-sqm derived.'
  )
}}

with source as (
    select * from {{ source('raw_booli', 'booli_listings') }}
),

renamed as (
    select
        cast(booliId as int64)                          as booli_id,
        cast(soldDate as date)                          as sold_date,
        cast(soldPrice as int64)                        as sold_price_sek,
        cast(listPrice as int64)                        as list_price_sek,
        cast(livingArea as float64)                     as living_area_sqm,
        cast(rooms as float64)                          as rooms,
        lower(trim(objectType))                         as object_type,
        cast(latitude as float64)                       as latitude,
        cast(longitude as float64)                      as longitude,
        trim(streetAddress)                             as street_address,
        trim(city)                                      as city,
        trim(county)                                    as county,
        trim(municipality)                              as municipality,

        -- Derived
        case
            when cast(livingArea as float64) > 0
            then round(cast(soldPrice as float64) / cast(livingArea as float64), 0)
            else null
        end                                             as price_per_sqm,

        case
            when cast(listPrice as int64) > 0
            then round(
                (cast(soldPrice as float64) - cast(listPrice as float64))
                / cast(listPrice as float64) * 100, 2
            )
            else null
        end                                             as price_vs_list_pct

    from source
    where booliId is not null
      and soldDate is not null
      and soldPrice > 0
)

select * from renamed
