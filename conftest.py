import sys
from pathlib import Path

ROOT = Path(__file__).parent

# Both test directories lack __init__.py (flat imports), so their
# source trees need to be on sys.path explicitly.
sys.path.insert(0, str(ROOT / "api"))        # exposes `app.*`
sys.path.insert(0, str(ROOT / "ingestion"))  # exposes `bostadspuls_ingest.*`
