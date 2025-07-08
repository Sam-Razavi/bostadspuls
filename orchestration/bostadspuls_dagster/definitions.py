"""Dagster Definitions — assembles all assets, jobs, schedules, and resources."""

from dagster import Definitions, load_assets_from_modules

from . import assets
from .resources import BigQueryResource
from .schedules import daily_schedule

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    schedules=[daily_schedule],
    resources={
        "bigquery": BigQueryResource(),
    },
)
