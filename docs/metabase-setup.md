# Metabase Setup

## Running locally

```bash
docker compose up metabase
```

Open http://localhost:3000 and complete the first-time setup wizard.

## Connecting to BigQuery

1. Go to **Admin → Databases → Add database**.
2. Select **BigQuery**.
3. Fill in:
   - **Display name:** `bostadspuls`
   - **Project ID:** your Google Cloud project ID
   - **Service account JSON:** paste the service account JSON (not base64)
   - **Default dataset:** `bostadspuls_marts`
4. Click **Save**.

## Saved questions (recommended)

Run these as saved questions and pin them to a dashboard:

### Quarterly price trends

```sql
SELECT
    period_start,
    county,
    avg_sold_price_sek,
    avg_price_per_sqm
FROM bostadspuls_marts.mart_price_trends
WHERE period_type = 'quarter'
ORDER BY period_start DESC, county
LIMIT 200
```

### Regional comparison

```sql
SELECT
    county,
    avg_price_per_sqm,
    total_sales,
    price_per_sqm_rank
FROM bostadspuls_marts.mart_regional_comparison
ORDER BY price_per_sqm_rank
```

## Embedding a dashboard

1. Go to **Admin → Settings → Embedding**.
2. Enable embedding and copy the `METABASE_SECRET_KEY`.
3. Add to your `.env`:
   ```
   METABASE_SECRET_KEY=...
   METABASE_SITE_URL=http://localhost:3000
   METABASE_DASHBOARD_ID=1
   ```
4. The Vue "Explore" view at `/explore` uses a signed iframe embed.
