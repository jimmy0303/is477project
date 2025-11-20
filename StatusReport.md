# StatusReport.md  
## Interim Status Report
### Project: Mapping U.S. AI Data Centers Against Grid Capacity  
### Team: Zhean Zhang & Qichen Shen

---

## 1. Overview

This interim status report summarizes our progress toward building an end-to-end workflow that integrates EPA eGRID data, EIA Form 860 capacity data, and an OSINT-based dataset of U.S. AI data centers. Since submitting our ProjectPlan.md, we have completed the acquisition of government datasets, developed a substantial portion of the OSINT dataset, begun integration scripts, produced a draft Snakemake workflow, created a structured repository, and started data quality and profiling work. This report documents the current state of these tasks, notes changes from the original plan, provides an updated timeline, and includes contribution statements from each team member.

---

## 2. Updates on Tasks From the Project Plan

### 2.1 Data Collection and Acquisition

**EPA eGRID 2023**  
Completed. We downloaded the official eGRID XLSX files, extracted the relevant tables (regional energy mix, emissions intensity, plant-level metadata), and converted them to CSV for easier integration. Data is stored under `data/raw/egrid_2023/`, along with a brief data-source description.

**EIA Form 860 (2024)**  
Completed. We downloaded the full EIA 860 generator-level datasets and extracted fields including generator capacity (MW), primary energy source, and latitude/longitude. Files are stored under `data/raw/eia860_2024/`. A schema mapping file has been drafted to document the relevant variables.

**OSINT AI Data Center Dataset**  
Approximately 85% complete. We collected ~240 public records from company announcements, DataCenterMap, Business Insider, and other open, publicly accessible reports. Each entry includes site name, address, company, coordinates, year announced, and estimated MW when available. A batch geocoding pipeline has been created to resolve missing coordinates, and remaining missing MW values are flagged for manual review.

---

### 2.2 Storage and Organization

Completed. The project now uses a clear folder structure:

```
data/
  raw/
  interim/
  processed/
scripts/
workflows/
docs/
notebooks/
results/
```

A `.gitignore` prevents accidental upload of large raw files. Repository documentation includes an early ERD showing the general relationships between data center locations, eGRID regions, and EIA balancing authorities.

---

### 2.3 Data Integration

Approximately 60% complete.  
We have successfully completed the first round of spatial joins between AI data center coordinates and eGRID subregions using GeoPandas. A preliminary integration script (`scripts/integrate_datasets.py`) merges OSINT records with regional energy-mix attributes and generator-level capacity values.

Challenges encountered so far:  
- Some data centers lie near boundaries between grid regions.  
- A few addresses yield ambiguous coordinates requiring manual verification.  
- Standardizing region identifiers across datasets required additional cleaning.

These issues are documented in `docs/integration_notes.md`.

---

### 2.4 Data Quality Assessment

Initial profiling completed.  
We generated summary statistics using Pandas Profiling to identify missing values, outliers, and inconsistencies. Early findings include:  
- About 12% of OSINT records lack MW capacity.  
- Incorrect outlier (6000 MW) corrected to 600 MW.  
- Inconsistent naming schemes for energy regions across datasets.

Further targeted checks will be completed before the final report.

---

### 2.5 Data Cleaning

Cleaning is ongoing.  
Progress so far includes standardization of company names, states, and region labels, removal of formatting inconsistencies, and harmonization of numeric fields. A cleaning notebook (`notebooks/01_data_cleaning.ipynb`) tracks all transformations made so far.

---

### 2.6 Workflow Automation

An early draft of the Snakemake workflow has been created. Current rules automate:  
- eGRID and EIA ingestion  
- OSINT cleaning  
- Initial dataset integration  

Files include:  
- `workflows/Snakefile`  
- `rules/acquire_data.smk`  
- `rules/clean_data.smk`  
- `rules/integrate.smk`

Rules for final analysis and plotting will be added in the next milestone.

---

### 2.7 Reproducibility and Transparency

Progress includes:  
- Creation of `requirements.txt` listing current dependencies  
- Draft metadata templates in `docs/metadata_template.md`  
- Box folder setup for hosting large raw datasets  
- Documentation on how to acquire eGRID and EIA datasets if redistribution is restricted

These steps establish the foundation for complete reproducibility in the final submission.

---

## 3. Changes to the Original Project Plan

### 3.1 Refined AI Data Center Inclusion Criteria
We revised our definition to include only explicitly AI-oriented facilities (AI, GPU clusters, HPC training centers). Generic cloud zones with no AI-specific indication were removed. This improves the validity of correlation analyses.

### 3.2 More Complex Region Mapping Than Expected
We originally planned to join datasets by state or county. However, because eGRID regions do not align with state boundaries, we shifted to polygon-based geospatial joins, increasing integration effort.

### 3.3 Adjusted Timeline Due to OSINT Complexity
OSINT sources often lacked complete or consistent information, requiring manual verification and slowing data preparation by about one week.

### 3.4 Integration of Grader Feedback
We strengthened metadata planning, clarified ethical considerations, and ensured all OSINT sources were publicly accessible with no login-restricted scraping.

---

## 4. Updated Timeline

| Task | Status | New Completion Date |
|------|--------|----------------------|
| Raw dataset acquisition | Complete | — |
| OSINT cleanup | In progress | Nov 14 |
| Geocoding | In progress | Nov 15 |
| Spatial integration | 60% complete | Nov 18 |
| Full data quality checks | Started | Nov 20 |
| Finalize Snakemake workflow | Early draft | Nov 25 |
| Analysis + visualizations | Not started | Nov 26–Dec 1 |
| Write final report | Not started | Dec 2–Dec 6 |
| Final GitHub release | — | Dec 7 |

---

## 5. Current Repository Artifacts

- `data/raw/egrid_2023/`  
- `data/raw/eia860_2024/`  
- `data/interim/osint_ai_centers.csv`  
- `scripts/geocode_osint.py`  
- `scripts/integrate_datasets.py`  
- `workflows/Snakefile`  
- `notebooks/01_data_cleaning.ipynb`  
- `docs/data_sources.md`  
- `docs/integration_notes.md`

These files represent the progress toward a fully automated data pipeline.

---

## 6. Contribution Statements

### Zhean Zhang  
I led the design of the pipeline architecture, collected and verified OSINT data, implemented the geocoding system, and created the initial spatial integration workflow. I built the Snakemake skeleton, organized the repository structure, drafted metadata templates, and documented integration challenges found so far.

### Qichen Shen  
Qichen focused on documentation, data profiling, and quality assessment. They developed the data cleaning and profiling notebook, standardized naming conventions across datasets, and created early versions of the data dictionary. They reviewed and verified OSINT entries and contributed to region-mapping validation.

---

## 7. Next Steps

1. Complete missing MW estimates and address remaining geocode issues.  
2. Resolve grid-region mismatches and refine spatial joins.  
3. Finalize Snakemake rules for analysis and visualization.  
4. Produce choropleths, correlation plots, and summary tables.  
5. Write the full README project report and metadata files.  
6. Validate complete reproduction instructions and Box file access.

---

## 8. Conclusion

The project is progressing on schedule, with all major datasets gathered and substantial progress made in cleaning, integration, and workflow development. Remaining tasks primarily involve analysis, visualization, and automation refinement. We expect to complete all remaining components before the final deadline.
