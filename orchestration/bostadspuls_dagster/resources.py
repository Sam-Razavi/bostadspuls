"""Dagster resource definitions."""

from bostadspuls_ingest.bigquery import get_client
from dagster import ConfigurableResource
from google.cloud import bigquery as bq


class BigQueryResource(ConfigurableResource):
    project: str = "bostadspuls"

    def get_client(self) -> bq.Client:
        return get_client(self.project)
