#!/usr/bin/env python
"""
integrate_datasets.py

Integrate cleaned OSINT, eGRID, and EIA data into:

1) Region-level summary table:
    data/processed/summary_regional_statistics.csv

2) Facility-level enriched table:
    data/processed/integrated_master_dataset.csv

Usage:
    python scripts/integrate_datasets.py
"""

import pandas as pd
from pathlib import Path

OSINT_PATH = Path("data/interim/osint_ai_cleaned.csv")
EGRID_PATH = Path("data/interim/egrid_cleaned.csv")
EIA_PATH = Path("data/interim/eia_cleaned.csv")

PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

REGION_OUT = PROC_DIR / "summary_regional_statistics.csv"
MASTER_OUT = PROC_DIR / "integrated_master_dataset.csv"


def main():
    osint = pd.read_csv(OSINT_PATH)
    egrid = pd.read_csv(EGRID_PATH)
    eia = pd.read_csv(EIA_PATH)

    # Ensure region_code columns
    for df in (osint, egrid, eia):
        if "region_code" in df.columns:
            df["region_code"] = df["region_code"].astype("string").str.strip().str.upper()

    # Region-level AI demand aggregation
    ai_region = osint.groupby("region_code", dropna=False).agg(
        ai_facility_count=("site_name", "count"),
        ai_total_mw=("estimated_power_mw", "sum"),
        ai_mw_median=("estimated_power_mw", "median"),
    )

    ai_region = ai_region.fillna(0)

    # Merge region-level electricity info
    region = ai_region.join(
        egrid.set_index("region_code"), how="left", rsuffix="_egrid"
    ).join(
        eia.set_index("region_code"), how="left", rsuffix="_eia"
    )

    # Compute AI-to-capacity ratios
    region["ai_share_of_capacity"] = (
        region["ai_total_mw"] / region["total_capacity_mw"]
    )

    # Sort for convenience
    region = region.reset_index().sort_values(
        by="ai_total_mw", ascending=False
    )

    region.to_csv(REGION_OUT, index=False)

    # Facility-level enriched: attach region attributes back to OSINT
    enriched = osint.merge(
        region,
        on="region_code",
        how="left",
        suffixes=("", "_region"),
    )

    enriched.to_csv(MASTER_OUT, index=False)

    print(f"Region summary written to {REGION_OUT}")
    print(f"Enriched facility-level dataset written to {MASTER_OUT}")


if __name__ == "__main__":
    main()
