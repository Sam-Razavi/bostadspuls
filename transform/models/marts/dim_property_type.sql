{{
  config(
    materialized='table',
    description='Property type dimension with Swedish and English labels.'
  )
}}

with types as (
    select distinct object_type
    from {{ ref('stg_booli__listings') }}
    where object_type is not null
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['object_type']) }} as property_type_key,
        object_type,
        case object_type
            when 'lägenhet'     then 'Apartment'
            when 'villa'        then 'Villa / Detached house'
            when 'radhus'       then 'Terraced house'
            when 'kedjehus'     then 'Semi-detached house'
            when 'parhus'       then 'Semi-detached house'
            when 'tomt'         then 'Plot'
            when 'fritidshus'   then 'Holiday home'
            when 'gård'         then 'Farm'
            else 'Other'
        end as object_type_en,
        case object_type
            when 'lägenhet'     then true
            else false
        end as is_apartment
    from types
)

select * from enriched
