# CITATIONS.md  
Bibliographic References for Data, Software, and Supporting Resources  
IS 477 Final Project · Fall 2025

---

## 🗂 Data Sources

### 1. EPA eGRID 2023
U.S. Environmental Protection Agency. 2023. **Emissions & Generation Resource Integrated Database (eGRID)**.  
Available at: https://www.epa.gov/egrid  
License: Public Domain (U.S. Federal Data)

> Used for: subregion capacity, fuel mix, emissions intensity, renewable share  
> Files in project: `data/raw/egrid_2023.csv`, processed to `data/interim/egrid_clean.csv`

---

### 2. U.S. Energy Information Administration (EIA) — Form 860 (2024 Edition)
U.S. Energy Information Administration. **Electricity Data — Form EIA-860 Detailed Data**, 2024 release.  
Available at: https://www.eia.gov/electricity/data/eia860/  
License: Public Domain (U.S. Federal Data)

> Used for: generator-level MW aggregation, renewable vs fossil breakdown  
> Files in project: `data/raw/eia860_2024.csv`, aggregated to `data/interim/eia_agg.csv`

---

### 3. OSINT AI Data Center Registry (Compiled Dataset)
Zhean Zhang & Qichen Shen. 2025. **Open-Source Intelligence (OSINT) Registry of U.S. AI Data Centers**, curated from public announcements, sustainability reports, industry filings, and news coverage.  
No proprietary or private data used.  
License: CC-BY 4.0 - Redistribution permitted with attribution.

> Files in project:  
> `data/raw/osint_ai_centers_raw.csv`  
> `data/interim/osint_ai_cleaned.csv`  
> `data/processed/integrated_master_dataset.csv`

---

## 📦 Software + Libraries

| Package | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core analysis |
| Pandas | ≥1.5 | Processing, integration |
| Numpy | ≥1.23 | Computation |
| Matplotlib | ≥3.7 | Visualization |
| Seaborn | ≥0.13 | Statistical plots |
| GeoPandas | ≥0.14 *(if installed)* | Choropleth mapping |
| Snakemake | ≥8.0 | Workflow automation |
| Conda / pip | latest | Environment management |

> Exact dependency snapshot can be reproduced using  
> `conda env create -f environment.yml` or `pip freeze > docs/pip_freeze.txt`.

---

## 📄 Additional References + Supporting Reading

Cambridge Power Research Council. *Grid Stress Under AI Energy Growth — Working Paper*, 2024.  
NVIDIA. *AI Infrastructure Scaling Considerations*, 2023.  
Google Data Center Sustainability Reports, 2022–2024.  
Meta & Microsoft High-Performance Compute Infrastructure Announcements, 2023–2025.  
AWS Public Utility Filing Summaries, 2022–2024.

(*All high-level references contain publicly accessible information; no NDA or restricted content used.*)

---

## Citation Format for Reuse

If referencing this project, please cite:

> Zhang, Z., & Shen, Q. (2025). *Mapping U.S. AI Data Centers Against Power Grid Capacity* — reproducible data workflow for IS477. University of Illinois Urbana-Champaign. GitHub: https://github.com/jimmy0303/is477project

