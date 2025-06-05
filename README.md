# Bostadspuls

A Swedish housing-market data platform. End-to-end data engineering:
ingestion → cloud warehouse → transformation → quality → API → dashboard.

## What it is

Bostadspuls ingests Swedish housing data from two public/semi-public sources,
models it into a cloud data warehouse, validates quality, and serves it through
an analytics API and an interactive Vue dashboard with a price heatmap of Sweden.

## Data sources

- **SCB (Statistics Sweden)** — free open API. Macro housing data: price indices,
  sales volumes, prices by region/municipality over time.
- **Booli** — listing-level data (price, size, rooms, location, sold date).
  Requires a free API key registered at booli.se/api.

## Tech stack

| Layer             | Technology                                        |
|-------------------|---------------------------------------------------|
| Ingestion         | Python 3.12 + httpx + Polars                      |
| Warehouse         | Google BigQuery (free tier)                       |
| Orchestration     | Dagster (software-defined assets)                 |
| Scheduling        | GitHub Actions cron                               |
| Transformation    | dbt (dbt-bigquery adapter)                        |
| Data quality      | dbt tests + Soda Core                             |
| API               | FastAPI                                           |
| Frontend          | Vue 3 + TypeScript + Vite + Apache ECharts        |
| BI (optional)     | Metabase connected to BigQuery                    |
| Deploy            | Railway (API) + Cloudflare Pages (frontend)       |

## Architecture

```
SCB API ─┐
         ├─► Polars ingestion ─► BigQuery (raw) ─► dbt ─► BigQuery (staging → marts)
Booli API┘         ▲                                        │
                   │ orchestrated by Dagster                ├─► FastAPI ─► Vue + ECharts
                   │ scheduled by GitHub Actions cron       └─► Metabase (optional)
```

## BigQuery datasets

- `bostadspuls_raw` — landed source data, untransformed
- `bostadspuls_staging` — dbt staging models
- `bostadspuls_marts` — star schema: `fact_sales`, `dim_location`,
  `dim_property_type`, `dim_date`, plus aggregate marts

## Repository structure

```
bostadspuls/
├── ingestion/          # Python + Polars ingestion package
│   ├── bostadspuls_ingest/
│   │   ├── scb.py
│   │   ├── booli.py
│   │   ├── bigquery.py
│   │   └── config.py
│   └── tests/
├── orchestration/      # Dagster project
│   └── bostadspuls_dagster/
├── transform/          # dbt project
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── dbt_project.yml
├── quality/            # Soda checks
├── api/                # FastAPI
│   └── app/
├── frontend/           # Vue 3 + ECharts
│   └── src/
├── .github/workflows/  # CI + scheduled pipeline
├── docker-compose.yml
└── README.md
```

## Quick start

```bash
# Install Python dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
```

## Environment variables

See `.env.example` for all required variables.

## License

MIT
