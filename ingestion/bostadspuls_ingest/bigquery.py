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


def load_scb_price_index(
    df: pl.DataFrame,
    client: bigquery.Client | None = None,
) -> None:
    """Append SCB price-index rows to bostadspuls_raw.scb_price_index."""
    load_dataframe(df, table_id="scb_price_index", client=client)
