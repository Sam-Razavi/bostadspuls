"""BigQuery client for loading Polars DataFrames into bostadspuls_raw.

Auth: set GOOGLE_APPLICATION_CREDENTIALS env var to a service-account JSON key,
or base64-encode the JSON and put it in GCP_SA_KEY — the client will decode it.
"""

from __future__ import annotations

import base64
import json
import os
import tempfile
from typing import Any

import polars as pl
from google.cloud import bigquery
from google.oauth2 import service_account

from .config import BIGQUERY_DATASET_RAW, BIGQUERY_PROJECT


def _get_credentials() -> service_account.Credentials | None:
    """Resolve credentials from GCP_SA_KEY (base64 JSON) or ADC."""
    raw = os.getenv("GCP_SA_KEY")
    if not raw:
        return None
    decoded = base64.b64decode(raw).decode()
    info = json.loads(decoded)
    return service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/bigquery"],
    )


def get_client(project: str = BIGQUERY_PROJECT) -> bigquery.Client:
    """Return an authenticated BigQuery client."""
    creds = _get_credentials()
    if creds:
        return bigquery.Client(project=project, credentials=creds)
    return bigquery.Client(project=project)


def ensure_dataset(client: bigquery.Client, dataset_id: str, location: str = "EU") -> None:
    """Create dataset if it does not exist."""
    dataset_ref = bigquery.Dataset(f"{client.project}.{dataset_id}")
    dataset_ref.location = location
    client.create_dataset(dataset_ref, exists_ok=True)


def load_dataframe(
    df: pl.DataFrame,
    table_id: str,
    dataset_id: str = BIGQUERY_DATASET_RAW,
    client: bigquery.Client | None = None,
    write_disposition: str = "WRITE_APPEND",
) -> bigquery.LoadJob:
    """Load a Polars DataFrame into a BigQuery table via Arrow.

    Uses Polars → PyArrow → BigQuery Storage Write API for efficiency.
    Automatically creates the dataset if needed.
    """
    bq = client or get_client()
    ensure_dataset(bq, dataset_id)

    table_ref = f"{bq.project}.{dataset_id}.{table_id}"
    arrow_table = df.to_arrow()

    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True,
    )

    job = bq.load_table_from_dataframe(
        df.to_pandas(),
        table_ref,
        job_config=job_config,
    )
    job.result()
    return job


def merge_dataframe(
    df: pl.DataFrame,
    table_id: str,
    merge_keys: list[str],
    dataset_id: str = BIGQUERY_DATASET_RAW,
    client: bigquery.Client | None = None,
) -> None:
    """Idempotent upsert: load df into a temp table then MERGE into target on merge_keys.

    Prevents duplicate rows on repeated pipeline runs.
    """
    bq = client or get_client()
    ensure_dataset(bq, dataset_id)

    tmp_table = f"{table_id}_tmp"
    load_dataframe(df, table_id=tmp_table, dataset_id=dataset_id, client=bq,
                   write_disposition="WRITE_TRUNCATE")

    target = f"`{bq.project}.{dataset_id}.{table_id}`"
    source = f"`{bq.project}.{dataset_id}.{tmp_table}`"

    on_clause = " AND ".join(f"T.{k} = S.{k}" for k in merge_keys)
    update_set = ", ".join(
        f"T.{c} = S.{c}" for c in df.columns if c not in merge_keys
    )
    insert_cols = ", ".join(df.columns)
    insert_vals = ", ".join(f"S.{c}" for c in df.columns)

    merge_sql = f"""
        MERGE {target} T
        USING {source} S
        ON {on_clause}
        WHEN MATCHED THEN
            UPDATE SET {update_set}
        WHEN NOT MATCHED THEN
            INSERT ({insert_cols}) VALUES ({insert_vals})
    """
    bq.query(merge_sql).result()
    bq.delete_table(f"{bq.project}.{dataset_id}.{tmp_table}", not_found_ok=True)


def load_scb_price_index(
    df: pl.DataFrame,
    client: bigquery.Client | None = None,
) -> None:
    """Idempotent upsert of SCB price-index rows keyed on (Region, quarter)."""
    merge_dataframe(df, table_id="scb_price_index", merge_keys=["Region", "quarter"],
                    client=client)


def load_booli_listings(
    df: pl.DataFrame,
    client: bigquery.Client | None = None,
) -> None:
    """Idempotent upsert of Booli listing rows keyed on (booliId, soldDate)."""
    merge_dataframe(
        df.with_columns(pl.col("soldDate").cast(pl.String)),
        table_id="booli_listings",
        merge_keys=["booliId", "soldDate"],
        client=client,
    )
