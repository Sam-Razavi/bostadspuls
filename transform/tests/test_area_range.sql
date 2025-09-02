-- Custom dbt test: living areas must be between 5 and 2000 sqm.
select *
from {{ ref('fact_sales') }}
where living_area_sqm is not null
  and (living_area_sqm < 5 or living_area_sqm > 2000)
