#!/usr/bin/env python
"""
clean_egrid.py

Clean and standardize EPA eGRID regional data.

Input:
    data/raw/egrid_2023.csv

Expected columns (you can adjust to your actual eGRID extract):
    region_code, total_generation_mwh,
    renewable_generation_mwh, fossil_generation_mwh,
    emissions_lbs_co2

Output:
    data/interim/egrid_cleaned.csv

Usage:
    python scripts/clean_egrid.py
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/egrid_2023.csv")
OUT_PATH = Path("data/interim/egrid_cleaned.csv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(RAW_PATH)

    df["region_code"] = df["region_code"].astype("string").str.strip().str.upper()

    numeric_cols = [
        "total_generation_mwh",
        "renewable_generation_mwh",
        "fossil_generation_mwh",
        "emissions_lbs_co2",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Compute renewable share
    df["renewable_share"] = df["renewable_generation_mwh"] / df["total_generation_mwh"]
    df["renewable_share"] = df["renewable_share"].clip(lower=0.0, upper=1.0)

    # Emissions intensity (lbs CO2 / MWh)
    df["emissions_intensity"] = df["emissions_lbs_co2"] / df["total_generation_mwh"]

    # Drop regions with no generation
    df = df[df["total_generation_mwh"] > 0]

    df.to_csv(OUT_PATH, index=False)
    print(f"Cleaned eGRID dataset written to {OUT_PATH}")


if __name__ == "__main__":
    main()
