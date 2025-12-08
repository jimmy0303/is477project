#!/usr/bin/env python
"""
clean_osint.py

Clean and standardize the OSINT AI data center registry.

Input:
    data/raw/osint_ai_centers_raw.csv

Expected columns (flexible, but recommended):
    company, site_name, address, city, state,
    latitude, longitude, estimated_power_mw,
    year_announced, region_code

Output:
    data/interim/osint_ai_cleaned.csv

Usage:
    python scripts/clean_osint.py
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/osint_ai_centers_raw.csv")
OUT_PATH = Path("data/interim/osint_ai_cleaned.csv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
    "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
    "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
    "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
    "WI","WY","DC",
}


def standardize_company(name: str) -> str:
    if not isinstance(name, str):
        return name
    return name.strip().replace("  ", " ")


def main():
    df = pd.read_csv(RAW_PATH)

    # Basic strip
    for col in ["company", "site_name", "address", "city", "state", "region_code"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Company
    if "company" in df.columns:
        df["company"] = df["company"].apply(standardize_company)

    # State codes
    if "state" in df.columns:
        df["state"] = df["state"].str.upper()
        df.loc[~df["state"].isin(VALID_STATES), "state"] = pd.NA

    # MW numeric
    if "estimated_power_mw" in df.columns:
        df["estimated_power_mw"] = (
            df["estimated_power_mw"]
            .astype("string")
            .str.replace("[^0-9.]", "", regex=True)
        )
        df["estimated_power_mw"] = pd.to_numeric(df["estimated_power_mw"], errors="coerce")

        # Remove clearly impossible values
        df.loc[(df["estimated_power_mw"] < 5) | (df["estimated_power_mw"] > 2000), "estimated_power_mw"] = pd.NA

    # Year
    if "year_announced" in df.columns:
        df["year_announced"] = pd.to_numeric(df["year_announced"], errors="coerce")
        df.loc[(df["year_announced"] < 2000) | (df["year_announced"] > 2050), "year_announced"] = pd.NA

    # Coordinates
    for col in ["latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop exact duplicates
    df = df.drop_duplicates(
        subset=["company", "site_name", "address", "city", "state"], keep="first"
    )

    # Simple region_code fallback if missing: mark as "UNKNOWN"
    if "region_code" not in df.columns:
        df["region_code"] = "UNKNOWN"
    else:
        df["region_code"] = df["region_code"].fillna("UNKNOWN")

    df.to_csv(OUT_PATH, index=False)
    print(f"Cleaned OSINT dataset written to {OUT_PATH}")


if __name__ == "__main__":
    main()
