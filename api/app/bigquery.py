"""BigQuery client singleton for the API."""

import os
from functools import lru_cache

from google.cloud import bigquery

BIGQUERY_PROJECT = os.getenv("BIGQUERY_PROJECT", "bostadspuls")
BIGQUERY_DATASET_MARTS = os.getenv("BIGQUERY_DATASET_MARTS", "bostadspuls_marts")


@lru_cache(maxsize=1)
def get_bq_client() -> bigquery.Client:
    return bigquery.Client(project=BIGQUERY_PROJECT)


def query(sql: str) -> list[dict]:
    client = get_bq_client()
    result = client.query(sql).result()
    return [dict(row) for row in result]


def marts_table(name: str) -> str:
    return f"`{BIGQUERY_PROJECT}.{BIGQUERY_DATASET_MARTS}.{name}`"
