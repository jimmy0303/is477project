# Metadata: Project and Datasets

This document provides high-level metadata for the project and the key datasets,
inspired by the DataCite and Schema.org schemas.

---

## 1. Project-Level Metadata

- **Title:** Mapping U.S. AI Data Centers Against Power Grid Capacity  
- **Creators:**  
  - Zhean (Jimmy) Zhang (zheanz2)  
  - Qichen Shen  
- **Affiliation:** University of Illinois Urbana-Champaign  
- **Course:** IS 477 – Data Management, Curation & Reproducible Research  
- **Publication Year:** 2025  
- **Version:** 1.0 (final-course-submission)  
- **Abstract:**  
  This project integrates public energy-system data with an open-source intelligence
  (OSINT) registry of AI-oriented data centers to examine the spatial relationship
  between AI infrastructure siting decisions and regional grid capacity and renewable
  energy availability.

- **Keywords:**  
  AI data centers, eGRID, EIA 860, grid capacity, renewable energy, reproducibility

- **Resource Type:** Dataset + Software + Technical Report  
- **Language:** English  

---

## 2. Dataset: EPA eGRID 2023

- **Title:** Emissions & Generation Resource Integrated Database (eGRID) 2023  
- **Publisher:** U.S. Environmental Protection Agency  
- **Resource Type:** Tabular data  
- **Format:** XLSX (original), CSV (derived)  
- **Access:** Downloaded manually from https://www.epa.gov/egrid  
- **License:** Public Domain (US Government Work)  
- **Role in Project:** Provides regional generation and emissions data.

---

## 3. Dataset: EIA Form 860 (2024)

- **Title:** Form EIA-860 Annual Electric Generator Report, 2024  
- **Publisher:** U.S. Energy Information Administration  
- **Resource Type:** Tabular data  
- **Format:** CSV bulk files  
- **Access:** Downloaded from https://www.eia.gov/electricity/data/eia860/  
- **License:** Public Domain  
- **Role in Project:** Provides generator-level capacity and fuel-type information.

---

## 4. Dataset: OSINT AI Data Center Registry

- **Title:** OSINT AI Data Center Registry (United States)  
- **Creators:** Project team (based on public sources)  
- **Resource Type:** Derived tabular data  
- **Format:** CSV  
- **Access:** Compiled manually from publicly available sources (company press releases, DataCenterMap, and news articles).  
- **License:** No proprietary data is redistributed; users should treat it as a convenience compilation and independently verify origin sources.  
- **Role in Project:** Identifies spatial distribution and approximate MW capacities of AI infrastructure.

---

## 5. Processed Datasets

- **Title:** Integrated AI–Grid Dataset  
- **Files:**  
  - `data/processed/integrated_master_dataset.csv`  
  - `data/processed/summary_regional_statistics.csv`  
- **Creator:** Project team  
- **Format:** CSV (UTF-8)  
- **Description:**  
  Machine-readable tables combining OSINT AI facility data with regional eGRID
  and EIA energy-system attributes. See `docs/data_dictionary.md` for schema.

---

## 6. Software and Workflow

- **Code:** Located under `scripts/` and `workflows/`.  
- **Workflow Engine:** Snakemake  
- **Environment:** Captured in `environment.yml` and `requirements.txt`.  
- **License:** MIT (see `LICENSE` file).  

---

## 7. Provenance and Reuse

- All transformations from raw → interim → processed tables are performed by
  the scripts in `scripts/` and orchestrated via `workflows/Snakefile`.  
- Detailed provenance notes are in `docs/provenance.md`.  
- Users may reuse the code under MIT and may reuse derived data where compatible
  with the licenses of the original sources.
