{{
  config(
    materialized='table',
    description='Conformed location dimension built from Booli listings.'
  )
}}

with locations as (
    select distinct
        county,
        municipality,
        city
    from {{ ref('stg_booli__listings') }}
    where county is not null
),

keyed as (
    select
        {{ dbt_utils.generate_surrogate_key(['county', 'municipality', 'city']) }}
            as location_key,
        county,
        municipality,
        city,
        -- Derive region_code from county name mapping
        case county
            when 'Stockholms län'         then 'SE-AB'
            when 'Uppsala län'            then 'SE-C'
            when 'Södermanlands län'      then 'SE-D'
            when 'Östergötlands län'      then 'SE-E'
            when 'Jönköpings län'         then 'SE-F'
            when 'Kronobergs län'         then 'SE-G'
            when 'Kalmar län'             then 'SE-H'
            when 'Gotlands län'           then 'SE-I'
            when 'Blekinge län'           then 'SE-K'
            when 'Skåne län'              then 'SE-M'
            when 'Hallands län'           then 'SE-N'
            when 'Västra Götalands län'   then 'SE-O'
            when 'Värmlands län'          then 'SE-S'
            when 'Örebro län'             then 'SE-T'
            when 'Västmanlands län'       then 'SE-U'
            when 'Dalarnas län'           then 'SE-W'
            when 'Gävleborgs län'         then 'SE-X'
            when 'Västernorrlands län'    then 'SE-Y'
            when 'Jämtlands län'          then 'SE-Z'
            when 'Västerbottens län'      then 'SE-AC'
            when 'Norrbottens län'        then 'SE-BD'
            else 'UNKNOWN'
        end as region_code
    from locations
)

select * from keyed
