"""Centralised application settings via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: str = ""
    bigquery_project: str = "bostadspuls"
    bigquery_dataset_marts: str = "bostadspuls_marts"


settings = Settings()
