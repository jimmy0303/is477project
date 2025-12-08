#!/usr/bin/env python
"""
analytics.py

Perform statistical analysis on the integrated dataset:

- Correlation between AI load and renewable share
- Simple linear regression: ai_total_mw ~ renewable_share + total_capacity_mw
- Region ranking export

Inputs:
    data/processed/summary_regional_statistics.csv

Outputs:
    results/tables/regression_summary.txt
    results/tables/capacity_region_ranking.csv

Usage:
    python scripts/analytics.py
"""

import pandas as pd
from pathlib import Path
import statsmodels.api as sm

REGION_PATH = Path("data/processed/summary_regional_statistics.csv")
RESULT_DIR = Path("results/tables")
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(REGION_PATH)

    # Basic correlation matrix (subset of variables)
    cols = [
        "ai_total_mw",
        "ai_facility_count",
        "total_capacity_mw",
        "renewable_share",
        "renewable_capacity_share",
        "emissions_intensity",
    ]
    corr = df[cols].corr()
    corr.to_csv(RESULT_DIR / "correlation_matrix.csv")

    # Simple linear regression
    # y: ai_total_mw
    # X: renewable_share, total_capacity_mw
    model_df = df[["ai_total_mw", "renewable_share", "total_capacity_mw"]].dropna()
    y = model_df["ai_total_mw"]
    X = model_df[["renewable_share", "total_capacity_mw"]]
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    with (RESULT_DIR / "regression_summary.txt").open("w", encoding="utf-8") as f:
        f.write(model.summary().as_text())

    # Region ranking by AI load and stress
    ranking = df.copy()
    ranking["ai_share_of_capacity"] = df["ai_share_of_capacity"]
    ranking = ranking.sort_values(
        by=["ai_share_of_capacity", "ai_total_mw"],
        ascending=[False, False],
    )

    ranking.to_csv(RESULT_DIR / "capacity_region_ranking.csv", index=False)

    print("Analytics complete. Outputs written to results/tables/")


if __name__ == "__main__":
    main()
