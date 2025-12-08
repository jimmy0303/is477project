#!/usr/bin/env python
"""
clean_eia.py

Clean and summarize EIA Form 860 generator-level data.

Input:
    data/raw/eia860_2024.csv

Expected useful columns:
    plant_id, plant_name, state, region_code, capacity_mw, fuel_type

Output:
    data/interim/eia_cleaned.csv
    (aggregated per region_code)

Usage:
    python scripts/clean_eia.py
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/eia860_2024.csv")
OUT_PATH = Path("data/interim/eia_cleaned.csv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

RENEWABLE_FUELS = {"WIND", "SOLAR", "HYDRO", "HYDROELECTRIC", "GEOTHERMAL", "BIOMASS"}


def main():
    df = pd.read_csv(RAW_PATH)

    for col in ["plant_name", "state", "region_code", "fuel_type"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().str.upper()

    df["capacity_mw"] = pd.to_numeric(df["capacity_mw"], errors="coerce")
    df = df[df["capacity_mw"] > 0]

    # Determine renewable / non-renewable
    df["is_renewable"] = df["fuel_type"].isin(RENEWABLE_FUELS)

    # Aggregate by region_code
    grouped = df.groupby("region_code", dropna=True).agg(
        total_capacity_mw=("capacity_mw", "sum"),
        renewable_capacity_mw=("capacity_mw", lambda s: s[df.loc[s.index, "is_renewable"]].sum()),
        plant_count=("plant_id", "nunique"),
    )

    grouped["renewable_capacity_share"] = (
        grouped["renewable_capacity_mw"] / grouped["total_capacity_mw"]
    ).replace([float("inf")], 0.0)

    grouped = grouped.reset_index()

    grouped.to_csv(OUT_PATH, index=False)
    print(f"Cleaned EIA aggregated dataset written to {OUT_PATH}")


if __name__ == "__main__":
    main()
