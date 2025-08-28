"""Dagster Definitions — assembles all assets, jobs, schedules, and resources."""

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from . import assets
from .dbt_assets import TRANSFORM_DIR, bostadspuls_dbt_assets
from .resources import BigQueryResource
from .schedules import daily_schedule

all_ingestion_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=[*all_ingestion_assets, bostadspuls_dbt_assets],
    schedules=[daily_schedule],
    resources={
        "bigquery": BigQueryResource(),
        "dbt": DbtCliResource(project_dir=str(TRANSFORM_DIR)),
    },
)
