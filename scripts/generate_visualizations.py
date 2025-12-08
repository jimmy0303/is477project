#!/usr/bin/env python
"""
generate_visualizations.py

Generate all final figures for the project based on the processed datasets.

Inputs:
    data/processed/summary_regional_statistics.csv
    data/processed/integrated_master_dataset.csv

Outputs (PNGs):
    results/figures/fig1_choropleth.png
    results/figures/fig2_scatter_mw_vs_renewable.png
    results/figures/fig3_heatmap.png
    results/figures/fig4_top10_power.png
    results/figures/fig5_renewable_vs_nonrenewable.png
    results/figures/fig6_timeseries_growth.png

Usage:
    python scripts/generate_visualizations.py
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

REGION_PATH = Path("data/processed/summary_regional_statistics.csv")
MASTER_PATH = Path("data/processed/integrated_master_dataset.csv")
FIG_DIR = Path("results/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig1_choropleth_bar(region_df: pd.DataFrame, outpath: Path):
    """
    Not a true GIS choropleth (no shapefile in this project),
    but a region-level bar plot approximating "AI MW by region".
    """
    df = region_df.sort_values("ai_total_mw", ascending=False).head(25)
    plt.figure(figsize=(10, 6))
    plt.bar(df["region_code"], df["ai_total_mw"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("AI Total MW")
    plt.title("AI Data Center Load by Grid Region")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def fig2_scatter(region_df: pd.DataFrame, outpath: Path):
    plt.figure(figsize=(8, 6))
    x = region_df["renewable_share"]
    y = region_df["ai_total_mw"]
    plt.scatter(x, y)
    plt.xlabel("Renewable Share (eGRID)")
    plt.ylabel("AI Total MW")
    plt.title("AI Load vs Renewable Share by Region")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def fig3_heatmap(region_df: pd.DataFrame, outpath: Path):
    """
    Simple heatmap of selected metrics across regions.
    """
    cols = ["ai_total_mw", "ai_facility_count", "total_capacity_mw",
            "renewable_share", "renewable_capacity_share", "emissions_intensity"]
    df = region_df[cols].corr()

    plt.figure(figsize=(8, 6))
    im = plt.imshow(df.values, aspect="auto")
    plt.colorbar(im)
    plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
    plt.yticks(range(len(cols)), cols)
    plt.title("Correlation Heatmap of Key Metrics")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def fig4_top10(region_df: pd.DataFrame, outpath: Path):
    df = region_df.sort_values("ai_total_mw", ascending=False).head(10)
    plt.figure(figsize=(8, 5))
    plt.barh(df["region_code"], df["ai_total_mw"])
    plt.xlabel("AI Total MW")
    plt.ylabel("Region Code")
    plt.title("Top 10 Regions by AI Load")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def fig5_renewable_vs_nonrenewable(region_df: pd.DataFrame, outpath: Path):
    df = region_df.copy()
    df["ai_in_renewable_dominant"] = np.where(
        df["renewable_share"] >= 0.5, df["ai_total_mw"], 0.0
    )
    df["ai_in_fossil_dominant"] = np.where(
        df["renewable_share"] < 0.5, df["ai_total_mw"], 0.0
    )
    totals = {
        "Renewable-dominant": df["ai_in_renewable_dominant"].sum(),
        "Fossil-dominant": df["ai_in_fossil_dominant"].sum(),
    }

    plt.figure(figsize=(6, 5))
    plt.bar(list(totals.keys()), list(totals.values()))
    plt.ylabel("AI Total MW")
    plt.title("AI Load in Renewable vs Fossil-Dominant Regions")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def fig6_timeseries(master_df: pd.DataFrame, outpath: Path):
    """
    Simple time-series: count and total MW by year_announced.
    """
    if "year_announced" not in master_df.columns:
        return

    df = master_df.dropna(subset=["year_announced"])
    df["year_announced"] = df["year_announced"].astype(int)
    grouped = df.groupby("year_announced").agg(
        facility_count=("site_name", "count"),
        total_mw=("estimated_power_mw", "sum"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(grouped["year_announced"], grouped["facility_count"], marker="o")
    ax1.set_xlabel("Year Announced")
    ax1.set_ylabel("Facility Count", color="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(grouped["year_announced"], grouped["total_mw"], marker="s")
    ax2.set_ylabel("Total MW", color="tab:orange")

    plt.title("AI Data Center Expansion Over Time")
    fig.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def main():
    region_df = pd.read_csv(REGION_PATH)
    master_df = pd.read_csv(MASTER_PATH)

    fig1_choropleth_bar(region_df, FIG_DIR / "fig1_choropleth.png")
    fig2_scatter(region_df, FIG_DIR / "fig2_scatter_mw_vs_renewable.png")
    fig3_heatmap(region_df, FIG_DIR / "fig3_heatmap.png")
    fig4_top10(region_df, FIG_DIR / "fig4_top10_power.png")
    fig5_renewable_vs_nonrenewable(region_df, FIG_DIR / "fig5_renewable_vs_nonrenewable.png")
    fig6_timeseries(master_df, FIG_DIR / "fig6_timeseries_growth.png")

    print("All figures generated in results/figures/")


if __name__ == "__main__":
    main()
