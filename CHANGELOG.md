# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.5.0] — 2025-10-31

### Added
- Pydantic Settings for typed, validated environment variable handling
- Structured logging and global exception handlers for the FastAPI API
- Deep `/health` endpoint with BigQuery liveness probe
- Per-endpoint rate limiting (slowapi, 60 req/min) to protect BigQuery quotas
- Non-root Docker user and two uvicorn workers for production hardening
- Nginx security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy) and gzip compression
- Frontend ESLint and vue-tsc type-check jobs in CI
- Post-deploy API smoke test in deploy workflow
- 404 Not Found page with router catch-all
- Consistent LoadingSpinner and ErrorAlert across all views
- robots.txt and favicon.svg
- SECURITY.md vulnerability disclosure policy
- Dependabot configuration for pip, npm, and GitHub Actions
- This CHANGELOG

## [0.4.0] — 2025-09-10

### Fixed
- Polars type inference bug: Region column forced to String dtype in `parse_scb_response`
- Test fixture column types corrected (Region/Tid must not carry `type: d`)
- pytest namespace collision between api/tests and ingestion/tests resolved
- CI now installs `[dev,api]` extras so FastAPI is available during test run
- All 16 ruff lint errors resolved (import order, unused imports, deprecated APIs, zip strict)

## [0.3.0] — 2025-08-28

### Added
- Year-over-year comparison view and API endpoint (`/compare`)
- Property-type breakdown view and API endpoint (`/property-types`)
- dbt marts: `mart_yoy_comparison`, `mart_property_type`
- Soda quality checks for both new marts
- Tenacity retry/backoff on SCB and Booli HTTP clients
- Dagster-dbt integration with `@dbt_assets` and `DbtCliResource`

## [0.2.0] — 2025-07-29

### Fixed
- Added `ingested_at` timestamp column to BigQuery raw tables
- Fixed incremental filter placement in `fact_sales.sql`
- Fixed `region_code` column reference in `mart_price_trends.sql`
- Added missing Vue Router entries for DistributionView and ExploreView
- Replaced duplicate region-code normalisation in `scb.py` with shared `regions.py` utility
- Corrected Docker build context from `./api` to repo root

## [0.1.0] — 2025-06-30

### Added
- SCB (Statistics Sweden) and Booli ingestion clients using httpx and Polars
- BigQuery raw table loader with MERGE-based upsert
- dbt staging, dimension, fact, and mart models
- Soda Core data quality checks on raw and mart layers
- Daily GitHub Actions pipeline (cron → ingest → dbt → soda)
- FastAPI with five endpoints: `/health`, `/trends`, `/regions`, `/property-types`, `/compare`
- TTL in-memory response cache
- Vue 3 + Vite + Pinia frontend with Tailwind CSS and ECharts visualisations
- Interactive Sweden choropleth map
- Metabase embedded dashboard view
- Docker multi-stage builds for API and frontend
- Railway + Cloudflare Pages deployment configuration
- Dagster orchestration with daily schedule
- Project scaffold: pyproject.toml, pytest, ruff, CI, deploy workflows
