-- Custom dbt test: no sold_date in the future.
select *
from {{ ref('fact_sales') }}
where sold_date > current_date()
