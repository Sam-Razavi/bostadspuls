"""Logging configuration for the Bostadspuls API."""

from __future__ import annotations

import logging
import sys


def configure_logging() -> None:
    """Configure root logger to emit structured lines to stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("google.auth").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
