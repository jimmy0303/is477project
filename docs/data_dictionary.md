# Data Dictionary

This document describes the main processed datasets produced by the project.

---

## 1. Facility-Level Dataset

**File:** `data/processed/integrated_master_dataset.csv`  
**Unit of observation:** Individual AI-oriented data center facility.

### Fields

| Field | Type | Description |
|---|---|---|
| company | string | Company or operator name (standardized). |
| site_name | string | Data center / campus name if available. |
| address | string | Street-level address where available. |
| city | string | City or locality. |
| state | string | Two-letter U.S. state code. |
| latitude | float | Latitude of the facility in decimal degrees. |
| longitude | float | Longitude of the facility in decimal degrees. |
| estimated_power_mw | float | Estimated total power capacity of the facility in MW. |
| year_announced | int | Year in which the facility was publicly announced. |
| region_code | string | Grid subregion code used for integration (derived from eGRID/EIA). |
| ai_facility_count | int | Number of AI facilities in the same region (region-level aggregate joined back). |
| ai_total_mw | float | Sum of estimated AI power demand in the region (MW). |
| ai_mw_median | float | Median power per AI facility in the region. |
| total_generation_mwh | float | Total electricity generation in the region (MWh, from eGRID). |
| renewable_generation_mwh | float | Total renewable electricity generation in the region (MWh). |
| fossil_generation_mwh | float | Total fossil-based electricity generation in the region (MWh). |
| renewable_share | float | Renewable generation share (0–1) in the region. |
| emissions_lbs_co2 | float | Regional CO₂ emissions in pounds. |
| emissions_intensity | float | Emissions intensity (lbs CO₂/MWh). |
| total_capacity_mw | float | Total generation capacity (MW) in the region (from EIA). |
| renewable_capacity_mw | float | Total renewable capacity (MW) in the region (from EIA). |
| renewable_capacity_share | float | Share of renewable capacity in the region (0–1). |
| plant_count | int | Number of power plants in the region. |
| ai_share_of_capacity | float | Ratio: AI total MW / total capacity MW in the region. |

---

## 2. Region-Level Dataset

**File:** `data/processed/summary_regional_statistics.csv`  
**Unit of observation:** Grid region.

### Fields

| Field | Type | Description |
|---|---|---|
| region_code | string | Grid subregion identifier (harmonized key). |
| ai_facility_count | int | Number of AI facilities in the region. |
| ai_total_mw | float | Sum of estimated AI power demand (MW). |
| ai_mw_median | float | Median facility power (MW). |
| total_generation_mwh | float | Total regional electricity generation (MWh). |
| renewable_generation_mwh | float | Total regional renewable generation (MWh). |
| fossil_generation_mwh | float | Total regional fossil-fuel generation (MWh). |
| renewable_share | float | Renewable generation share in regional generation (0–1). |
| emissions_lbs_co2 | float | Total CO₂ emissions from electricity generation (lbs). |
| emissions_intensity | float | Emissions intensity (lbs CO₂/MWh). |
| total_capacity_mw | float | Total generation capacity (MW). |
| renewable_capacity_mw | float | Total renewable generation capacity (MW). |
| renewable_capacity_share | float | Renewable capacity share in total capacity (0–1). |
| plant_count | int | Number of power plants in the region. |
| ai_share_of_capacity | float | Ratio of AI load (MW) to regional generation capacity. |

---

## 3. Raw and Interim Datasets

High-level descriptions of raw/interim datasets are provided in `docs/metadata_full.md`.  
All column names are documented in comments in the cleaning scripts under `scripts/`.
