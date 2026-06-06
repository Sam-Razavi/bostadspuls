# BigQuery Schema

## Dataset: `bostadspuls_raw`

Raw source data, landed as-is from external APIs. Never modified after write.

### `scb_price_index`

| Column       | Type    | Description                                  |
|--------------|---------|----------------------------------------------|
| Region       | STRING  | SCB numeric region code (e.g. "0180")        |
| quarter      | STRING  | Quarter in SCB format (e.g. "2024K1")        |
| region_code  | STRING  | ISO 3166-2:SE county code (e.g. "SE-AB")     |
| price_index  | FLOAT64 | Residential property price index (base=100)  |

Merge key: `(Region, quarter)`

### `scb_sales_volume`

| Column       | Type  | Description                              |
|--------------|-------|------------------------------------------|
| Region       | STRING | SCB numeric region code                 |
| quarter      | STRING | Quarter in SCB format                   |
| region_code  | STRING | ISO 3166-2:SE county code               |
| sales_count  | INT64  | Number of residential sales in quarter  |

Merge key: `(Region, quarter)`

### `booli_listings`

| Column         | Type    | Description                            |
|----------------|---------|----------------------------------------|
| booliId        | INT64   | Booli unique listing identifier        |
| soldDate       | DATE    | Date the property was sold             |
| soldPrice      | INT64   | Sold price in SEK                      |
| listPrice      | INT64   | Listed price in SEK                    |
| livingArea     | FLOAT64 | Living area in square metres           |
| rooms          | FLOAT64 | Number of rooms                        |
| objectType     | STRING  | Property type (Lägenhet, Villa, etc.)  |
| latitude       | FLOAT64 | WGS-84 latitude                        |
| longitude      | FLOAT64 | WGS-84 longitude                       |
| county         | STRING  | County name                            |
| municipality   | STRING  | Municipality name                      |
| ingested_at    | TIMESTAMP | Row insertion timestamp              |

Merge key: `(booliId, soldDate)`

## Dataset: `bostadspuls_staging`

Light cleaning and renaming only — no aggregation, no joins.
See `transform/models/staging/` for definitions.

## Dataset: `bostadspuls_marts`

Star schema and analytics marts. See `transform/models/marts/` for definitions.

### Core tables

- `fact_sales` — grain: one sold property
- `dim_location` — conformed location dimension
- `dim_property_type` — property type dimension
- `dim_date` — calendar dimension (date spine)
- `mart_price_trends` — quarterly aggregates
- `mart_regional_comparison` — cross-county comparison
