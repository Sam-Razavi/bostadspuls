"""Configuration loaded from environment variables."""

import os

SCB_BASE_URL = "https://api.scb.se/OV0104/v1/doris/sv/ssd"

BIGQUERY_PROJECT = os.getenv("BIGQUERY_PROJECT", "bostadspuls")
BIGQUERY_DATASET_RAW = os.getenv("BIGQUERY_DATASET_RAW", "bostadspuls_raw")
BIGQUERY_DATASET_MARTS = os.getenv("BIGQUERY_DATASET_MARTS", "bostadspuls_marts")

BOOLI_CALLER_ID = os.getenv("BOOLI_CALLER_ID", "")
BOOLI_KEY = os.getenv("BOOLI_KEY", "")
BOOLI_BASE_URL = "https://api.booli.se"
