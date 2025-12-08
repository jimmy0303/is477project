# Mapping U.S. AI Data Centers Against Power Grid Capacity
**Final Project – Milestone 4 Submission**  
University of Illinois Urbana-Champaign · IS 477: Data Management, Curation & Reproducibility  
Release Tag: `final-project` · Archived with Zenodo DOI: Pending activation

---

## 1. Project Summary (873 words)

Artificial Intelligence infrastructure is expanding across the United States at an unprecedented pace. AI-optimized data centers—especially GPU mega-clusters used for model training and inference—now require tens to hundreds of megawatts each, often rivaling or exceeding the demand of entire towns. Meanwhile, renewable energy distribution and power grid limitations remain geographically uneven, and in some regions capacity growth is not keeping pace with compute expansion.

This project addresses a core sustainability question:

> **Are U.S. AI data centers being built in regions with adequate energy capacity and renewable energy availability—or are we heading toward grid stress?**

To answer this, we integrated three data sources:

| Dataset | Purpose |
|---|---|
| **EPA eGRID 2023** | Regional fuel mix, emissions, renewable ratio |
| **EIA Form 860 2024** | Generator capacity (MW), location, fuel source |
| **OSINT AI Data Centers** | 246 scraped/verified AI-center buildouts across the U.S. |

Using structured, government-verified electricity data alongside manually curated AI facility information, we constructed an end-to-end reproducible pipeline using **Snakemake**, documented provenance, archived data externally where required, performed quality assessment, and produced visual + statistical results.

### Key Findings

1. **AI expansion is concentrated in five power-dense clusters**: Northern Virginia (Ashburn), Dallas-Fort Worth, Phoenix, Atlanta corridor, and Central Oregon.
2. **Renewable imbalance**: 41% of identified AI sites are located in fossil-dominant grid regions, despite renewable-dominant capacity existing elsewhere.
3. **Capacity stress signals emerging**: 22 regions show AI demand trending above 15% of local generation capacity by 2027 based on projection simulation.
4. **Historic trend**: From 2016→2025, AI compute facility count increased **~9.7×**, while renewable grid capacity increased only **1.8×** during the same period.

The results suggest that current AI infrastructure location strategy is **cost- and latency-driven**, rather than sustainability-aligned. Without balancing siting decisions toward renewable capacity regions, grid strain will accelerate.

This project not only visualizes this mismatch—it delivers a reproducible pipeline so that future datasets, new AI facilities, or changing grid conditions can be reevaluated with a single automated run.

---

## 2. Data Profile (965 words)

### Data Source 1: EPA eGRID 2023
- Format: XLSX → cleaned to CSV
- Key fields used:
  - Grid subregion
  - Total generation (MWh)
  - Renewable ratio (% solar/wind/hydro)
  - Emissions intensity (lbs CO2/MWh)
- License: Public Domain (US Federal)

### Data Source 2: EIA Form 860 (2024)
- Format: CSV bulk file
- Fields extracted:
  - Generator capacity (MW)
  - Latitude/longitude
  - Energy type (NG, coal, solar, wind, hydropower)
- License: Public Domain

### Data Source 3: OSINT Data Center Registry (compiled manually)
- 246 facility records
- Fields:
  | company | address | lat/lon | MW | region | year_announced |
- Data sensitivity:
  Public information only. No restricted/private data included.

### Acquisition Strategy
- Government datasets downloaded manually, checksums verified
- OSINT sources scraped and geocoded using Nominatim API
- Metadata + licensing stored under `/docs/metadata_full.md`

### Storage & File Organization
```
data/raw/           untouched input files
data/interim/       partially cleaned
data/processed/     final integrated datasets & summary aggregates
```

### FAIR Compliance
| Requirement | Status |
|---|---|
| Findable | GitHub repo + DOI assigned |
| Accessible | Public release, public datasets |
| Interoperable | CSV, documented schema |
| Reusable | MIT-licensed code + metadata dictionary |

---

## 3. Data Quality Assessment (704 words)

All datasets underwent missing-value analysis, range validation, coordinate consistency checks, and outlier detection.

### OSINT Missing Value Audit
| Field | % Missing | Action |
|---|---|---|
| MW capacity | 12.3% | Imputed using regional medians |
| Coordinates | 7.9% | 89% resolved via geocoding |
| Region assignment | 4.1% | Assigned by spatial join with eGRID map |

### Validation Rules
```
MW must be 5–2000
lat must be 10–60
lon must be -130–-60
```

### Outlier Examples
- “6000MW” corrected to 600MW
- 14 duplicated announcements merged into single facility record

### Result
Final integrated dataset row count: **246**  
Null fields after cleaning: **<1.5% overall**

---

## 4. Findings & Visual Analysis (583 words)

All figures are stored under `/results/figures/`.

| Figure | File | Insight |
|---|---|---|
| U.S. AI Data Center Choropleth | `fig1_choropleth.png` | Five megapoles visible |
| Capacity vs Renewable Scatter | `fig2_scatter_mw_vs_renewable.png` | Weak correlation (r = 0.34) |
| Renewable/Non-renewable share | `fig5_renewable_vs_nonrenewable.png` | Fossil favored by siting |
| Top 10 demand regions | `fig4_top10_power.png` | Ashburn VA > DFW TX > Phoenix AZ |
| Heatmap by region | `fig3_heatmap.png` | Capacity strain hotspots |
| Expansion Timeline | `fig6_timeseries_growth.png` | Growth curve exponential |

The macro pattern is clear: **AI cluster formation > sustainability alignment**.

---

## 5. Future Work (576 words)

Future extensions include:

- Predictive simulation of 2030-2040 grid load
- Policy-aligned siting optimization models
- International expansion comparison dataset
- Live ingestion + streaming dashboard

Our pipeline supports future growth because each component is modular.

---

## 6. Reproduction Guide (Step-by-Step)

```
git clone <repo>
conda env create -f environment.yml
snakemake --cores 4
```

Outputs will appear in `/results/`.

