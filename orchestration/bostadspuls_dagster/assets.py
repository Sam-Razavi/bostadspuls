"""Software-defined assets for SCB and Booli ingestion."""

from __future__ import annotations

import asyncio

from dagster import AssetExecutionContext, DailyPartitionsDefinition, asset

from bostadspuls_ingest.bigquery import load_booli_listings, load_scb_price_index
from bostadspuls_ingest.booli import BooliClient, parse_booli_listings
from bostadspuls_ingest.scb import SCBClient, parse_price_index

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")


@asset(
    group_name="ingestion",
    description="SCB housing price index by region and quarter, loaded into bostadspuls_raw.",
)
def scb_price_index(context: AssetExecutionContext) -> None:
    client = SCBClient()
    data = asyncio.run(client.fetch_price_index())
    df = parse_price_index(data)
    context.log.info(f"Parsed {len(df)} SCB price-index rows")
    load_scb_price_index(df)
    context.log.info("Loaded into bostadspuls_raw.scb_price_index")


@asset(
    group_name="ingestion",
    description="Booli sold listings by date, loaded into bostadspuls_raw.",
    deps=[scb_price_index],
)
def booli_listings(context: AssetExecutionContext) -> None:
    client = BooliClient()
    raw = client.fetch_sold_all_pages()
    df = parse_booli_listings(raw)
    context.log.info(f"Parsed {len(df)} Booli listing rows")
    load_booli_listings(df)
    context.log.info("Loaded into bostadspuls_raw.booli_listings")
