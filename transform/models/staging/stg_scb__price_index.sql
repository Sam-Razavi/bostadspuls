{{
  config(
    materialized='view',
    description='Staged SCB price index: renamed, cast, and lightly cleaned.'
  )
}}

with source as (
    select * from {{ source('raw_scb', 'scb_price_index') }}
),

renamed as (
    select
        Region                                          as scb_region_code,
        quarter                                         as scb_quarter,
        -- Parse SCB quarter format "2024K1" → DATE of first day of quarter
        parse_date(
            '%Y-%m-%d',
            concat(
                substr(quarter, 1, 4), '-',
                case substr(quarter, 6, 1)
                    when '1' then '01'
                    when '2' then '04'
                    when '3' then '07'
                    when '4' then '10'
                end,
                '-01'
            )
        )                                               as quarter_start_date,
        coalesce(region_code, 'UNKNOWN')                as region_code,
        cast(price_index as float64)                    as price_index
    from source
    where price_index is not null
)

select * from renamed
