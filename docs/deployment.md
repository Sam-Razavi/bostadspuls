# Deployment Architecture

## Services

| Service  | Platform          | URL                                         |
|----------|-------------------|---------------------------------------------|
| API      | Railway           | https://bostadspuls-api.up.railway.app      |
| Frontend | Cloudflare Pages  | https://bostadspuls.pages.dev               |
| Pipeline | GitHub Actions    | cron (no always-on server)                  |
| Metabase | optional / local  | http://localhost:3000                        |

## Railway — API

1. Create a new Railway project and service.
2. Set the following **environment variables** in the Railway dashboard:
   - `GCP_SA_KEY` — base64-encoded service account JSON
   - `BIGQUERY_PROJECT` — your GCP project ID
   - `CORS_ORIGINS` — `https://bostadspuls.pages.dev`
3. Railway reads `railway.json` for the build and start commands.
4. CI deploys on every push to `main` via the `RAILWAY_TOKEN` secret.

## Cloudflare Pages — Frontend

1. Connect the repository to a new Cloudflare Pages project named `bostadspuls`.
2. Build settings:
   - **Framework preset:** None (Vite)
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** `frontend`
3. Environment variables:
   - `VITE_API_URL` — Railway API URL
4. SPA routing is handled by `frontend/public/_redirects`.

## Required GitHub Secrets

| Secret                  | Used by              |
|-------------------------|----------------------|
| `GCP_SA_KEY`            | pipeline, dbt        |
| `BIGQUERY_PROJECT`      | pipeline, dbt        |
| `BOOLI_CALLER_ID`       | pipeline             |
| `BOOLI_KEY`             | pipeline             |
| `RAILWAY_TOKEN`         | deploy-api job       |
| `CLOUDFLARE_API_TOKEN`  | deploy-frontend job  |
| `CLOUDFLARE_ACCOUNT_ID` | deploy-frontend job  |
| `VITE_API_URL`          | deploy-frontend job  |
