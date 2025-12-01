# Bostadspuls

**Swedish housing-market data platform** — end-to-end data engineering from raw API ingestion to an interactive Vue dashboard with a live price heatmap of Sweden.

[![CI](https://github.com/Sam-Razavi/bostadspuls/actions/workflows/ci.yml/badge.svg)](https://github.com/Sam-Razavi/bostadspuls/actions/workflows/ci.yml)
[![Pipeline](https://github.com/Sam-Razavi/bostadspuls/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Sam-Razavi/bostadspuls/actions/workflows/pipeline.yml)

## What it does

1. **Ingest** housing data daily from SCB (Statistics Sweden) and Booli (listing portal).
2. **Land** raw data in Google BigQuery (`bostadspuls_raw`).
3. **Transform** with dbt into a star schema (`bostadspuls_staging` → `bostadspuls_marts`).
4. **Validate** with dbt tests + Soda Core scans — pipeline fails on quality errors.
5. **Serve** via a FastAPI analytics API.
6. **Visualise** in a Vue 3 dashboard: price trends, regional comparison, and a choropleth heatmap.

## Architecture

```
SCB API ─┐
         ├─► Polars ingestion ─► BigQuery (raw) ─► dbt ─► BigQuery (staging → marts)
Booli API┘         ▲                                        │
                   │ orchestrated by Dagster                ├─► FastAPI ─► Vue + ECharts
                   │ scheduled by GitHub Actions cron       └─► Metabase (optional)
```

## Tech stack

| Layer            | Technology                                       |
|------------------|--------------------------------------------------|
| Ingestion        | Python 3.12 · httpx · Polars                     |
| Warehouse        | Google BigQuery (free tier)                      |
| Orchestration    | Dagster (software-defined assets)                |
| Scheduling       | GitHub Actions cron                              |
| Transformation   | dbt-bigquery                                     |
| Data quality     | dbt tests · Soda Core                            |
| API              | FastAPI · Pydantic v2                            |
| Frontend         | Vue 3 · TypeScript · Vite · Apache ECharts       |
| BI (optional)    | Metabase                                         |
| Deploy           | Railway (API) · Cloudflare Pages (frontend)      |

## Data sources

- **SCB** — free PxWeb API. Quarterly price indices and sales volumes by county/municipality.
- **Booli** — individual sold listings (price, sqm, rooms, location). Free API key from booli.se/api.

## Quick start

```bash
# Clone
git clone https://github.com/Sam-Razavi/bostadspuls.git
cd bostadspuls

# Python environment
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Copy and fill in env vars
cp .env.example .env

# Run ingestion tests
pytest

# Run linter
ruff check .
```

### Full local stack with Docker

```bash
cp .env.example .env   # fill in GCP_SA_KEY etc.
docker compose up
```

| Service   | URL                       |
|-----------|---------------------------|
| API       | http://localhost:8000     |
| Frontend  | http://localhost:5173     |
| Metabase  | http://localhost:3000     |

### dbt

```bash
cd transform
cp ../profiles.yml.example ~/.dbt/profiles.yml  # edit for your project
dbt deps
dbt run
dbt test
```

## Environment variables

See `.env.example` for the full list. Key variables:

| Variable               | Description                                   |
|------------------------|-----------------------------------------------|
| `GCP_SA_KEY`           | Base64-encoded GCP service account JSON       |
| `BIGQUERY_PROJECT`     | GCP project ID                                |
| `BOOLI_CALLER_ID`      | Booli API caller ID                           |
| `BOOLI_KEY`            | Booli API key                                 |
| `VITE_API_URL`         | FastAPI base URL for the frontend             |

## Repository layout

```
bostadspuls/
├── ingestion/          # Python + Polars ingestion (SCB + Booli)
├── orchestration/      # Dagster software-defined assets
├── transform/          # dbt project (staging → marts)
├── quality/            # Soda Core check files
├── api/                # FastAPI analytics API
├── frontend/           # Vue 3 + ECharts dashboard
├── docs/               # Architecture + deployment docs
├── .github/workflows/  # CI, daily pipeline, deploy
├── docker-compose.yml
└── railway.json
```

## Deployment

See [docs/deployment.md](docs/deployment.md) for Railway + Cloudflare Pages setup.

## License

MIT — see [LICENSE](LICENSE).
