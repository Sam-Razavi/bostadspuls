"""Region code normalization utilities for Swedish administrative codes.

SCB uses numeric region codes (e.g., "0180" for Stockholm city).
We normalize these to ISO 3166-2:SE county codes for consistent joins.
"""

from __future__ import annotations

import polars as pl

# SCB county (lan) prefix → ISO 3166-2:SE
COUNTY_CODE_MAP: dict[str, str] = {
    "01": "SE-AB",  # Stockholms län
    "03": "SE-C",   # Uppsala län
    "04": "SE-D",   # Södermanlands län
    "05": "SE-E",   # Östergötlands län
    "06": "SE-F",   # Jönköpings län
    "07": "SE-G",   # Kronobergs län
    "08": "SE-H",   # Kalmar län
    "09": "SE-I",   # Gotlands län
    "10": "SE-K",   # Blekinge län
    "12": "SE-M",   # Skåne län
    "13": "SE-N",   # Hallands län
    "14": "SE-O",   # Västra Götalands län
    "17": "SE-S",   # Värmlands län
    "18": "SE-T",   # Örebro län
    "19": "SE-U",   # Västmanlands län
    "20": "SE-W",   # Dalarnas län
    "21": "SE-X",   # Gävleborgs län
    "22": "SE-Y",   # Västernorrlands län
    "23": "SE-Z",   # Jämtlands län
    "24": "SE-AC",  # Västerbottens län
    "25": "SE-BD",  # Norrbottens län
}

# Human-readable county names keyed by ISO code
COUNTY_NAMES: dict[str, str] = {
    "SE-AB": "Stockholms län",
    "SE-C": "Uppsala län",
    "SE-D": "Södermanlands län",
    "SE-E": "Östergötlands län",
    "SE-F": "Jönköpings län",
    "SE-G": "Kronobergs län",
    "SE-H": "Kalmar län",
    "SE-I": "Gotlands län",
    "SE-K": "Blekinge län",
    "SE-M": "Skåne län",
    "SE-N": "Hallands län",
    "SE-O": "Västra Götalands län",
    "SE-S": "Värmlands län",
    "SE-T": "Örebro län",
    "SE-U": "Västmanlands län",
    "SE-W": "Dalarnas län",
    "SE-X": "Gävleborgs län",
    "SE-Y": "Västernorrlands län",
    "SE-Z": "Jämtlands län",
    "SE-AC": "Västerbottens län",
    "SE-BD": "Norrbottens län",
}

_mapping_df: pl.DataFrame | None = None


def _get_mapping_df() -> pl.DataFrame:
    global _mapping_df
    if _mapping_df is None:
        _mapping_df = pl.DataFrame(
            {
                "prefix": list(COUNTY_CODE_MAP.keys()),
                "region_code": list(COUNTY_CODE_MAP.values()),
            }
        )
    return _mapping_df


def add_region_code(df: pl.DataFrame, region_col: str = "Region") -> pl.DataFrame:
    """Join ISO county code onto a DataFrame using the first two digits of region_col."""
    if region_col not in df.columns:
        return df
    mapping = _get_mapping_df()
    return (
        df.with_columns(pl.col(region_col).str.slice(0, 2).alias("_prefix"))
        .join(mapping.rename({"prefix": "_prefix"}), on="_prefix", how="left")
        .drop("_prefix")
    )


def add_county_name(df: pl.DataFrame, region_code_col: str = "region_code") -> pl.DataFrame:
    """Join human-readable county name onto a DataFrame via region_code_col."""
    if region_code_col not in df.columns:
        return df
    name_df = pl.DataFrame(
        {
            region_code_col: list(COUNTY_NAMES.keys()),
            "county_name": list(COUNTY_NAMES.values()),
        }
    )
    return df.join(name_df, on=region_code_col, how="left")
