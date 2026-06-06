-- Custom dbt test: no sold prices below 50,000 SEK (likely data error)
-- Returns rows that violate the threshold.
select *
from {{ ref('fact_sales') }}
where sold_price_sek < 50000
