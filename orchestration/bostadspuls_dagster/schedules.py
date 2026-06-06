"""Dagster schedules for the bostadspuls pipeline."""

from dagster import AssetSelection, ScheduleDefinition, define_asset_job

ingestion_job = define_asset_job(
    name="ingestion_job",
    selection=AssetSelection.groups("ingestion"),
)

daily_schedule = ScheduleDefinition(
    name="daily_ingestion_schedule",
    cron_schedule="0 6 * * *",
    job=ingestion_job,
    execution_timezone="Europe/Stockholm",
)
