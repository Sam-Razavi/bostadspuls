"""Dagster resource definitions."""

from dagster import ConfigurableResource
from google.cloud import bigquery as bq

from bostadspuls_ingest.bigquery import get_client


class BigQueryResource(ConfigurableResource):
    project: str = "bostadspuls"

    def get_client(self) -> bq.Client:
        return get_client(self.project)
