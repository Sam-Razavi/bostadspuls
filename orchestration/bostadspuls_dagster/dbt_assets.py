"""dagster-dbt integration: runs the full dbt build as a Dagster asset group."""

from __future__ import annotations

from pathlib import Path

from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

REPO_ROOT = Path(__file__).parent.parent.parent
TRANSFORM_DIR = REPO_ROOT / "transform"

bostadspuls_dbt_project = DbtProject(
    project_dir=TRANSFORM_DIR,
    packaged_project_dir=TRANSFORM_DIR,
)
bostadspuls_dbt_project.prepare_if_dev()


@dbt_assets(manifest=bostadspuls_dbt_project.manifest_path)
def bostadspuls_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
