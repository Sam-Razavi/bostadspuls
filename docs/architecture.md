# Architecture

## Data lineage

```
SCB PxWeb API
    │
    ▼ httpx async fetch
bostadspuls_raw.scb_price_index
    │
    ▼ dbt view
bostadspuls_staging.stg_scb__price_index
    │
    └──────────────────────────────┐
                                   │
Booli REST API                     │
    │                              │
    ▼ httpx + HMAC auth            │
bostadspuls_raw.booli_listings     │
    │                              │
    ▼ dbt view                     │
bostadspuls_staging.stg_booli__listings
    │
    ├─► dim_location (county, municipality, city)
    ├─► dim_property_type (lägenhet, villa, …)
    ├─► dim_date (date spine 2020–2030)
    │
    ▼ dbt incremental table
bostadspuls_marts.fact_sales
    │
    ├─► mart_price_trends (monthly + quarterly aggregates)
    └─► mart_regional_comparison (trailing 12m per county)
                │
                ▼
          FastAPI /trends  /regions  /regions/{code}
                │
                ▼
      Vue 3 dashboard
      ├── TrendsView (line chart)
      ├── RegionsView (bar chart)
      ├── MapView (ECharts choropleth)
      └── ExploreView (Metabase iframe)
```

## Orchestration flow

1. GitHub Actions cron triggers at 05:00 UTC.
2. Ingestion job: SCB fetch → BigQuery merge; Booli fetch → BigQuery merge.
3. Transform job: `dbt run` + `dbt test` + Soda Core scans.
4. On failure at any step, the workflow fails and sends a notification.
5. Dagster (optional local) provides the same asset graph with a UI.

## Incremental strategy

`fact_sales` uses dbt incremental (`unique_key=booli_id`, `merge`).  
On each run it processes only rows where `sold_date >= CURRENT_DATE - 3 DAYS`,
handling late Booli data arrivals without full-refresh cost.

## Security

- GCP service account has **BigQuery Data Editor + Job User** only — no broader access.
- Booli credentials stored in GitHub Secrets; never committed.
- FastAPI has CORS restricted to the frontend origin via `CORS_ORIGINS`.
