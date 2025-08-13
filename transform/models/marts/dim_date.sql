{{
  config(
    materialized='table',
    description='Calendar date dimension generated from a date spine (2020-01-01 onward).'
  )
}}

{{
  dbt_date.get_date_dimension(
    start_date="2020-01-01",
    end_date="2030-12-31"
  )
}}
