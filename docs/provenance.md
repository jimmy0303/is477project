# Provenance

This document explains how we capture both **prospective** and **retrospective**
provenance for the project.

---

## 1. Prospective Provenance (Planned Workflow)

Prospective provenance describes the *intended* sequence of steps in the analysis.

- The workflow is expressed as a **Snakemake** pipeline in `workflows/Snakefile`.
- Each rule defines:
  - Input files
  - Output files
  - The script used to transform inputs into outputs

High-level flow:

1. `data/raw/*.csv` – manually downloaded or compiled inputs  
2. `scripts/clean_osint.py` → `data/interim/osint_ai_cleaned.csv`  
3. `scripts/clean_egrid.py` → `data/interim/egrid_cleaned.csv`  
4. `scripts/clean_eia.py` → `data/interim/eia_cleaned.csv`  
5. `scripts/integrate_datasets.py` → processed datasets  
6. `scripts/analytics.py` → summary statistics and rankings  
7. `scripts/generate_visualizations.py` → final figures

The prospective provenance is therefore encoded in the Snakefile as a
directed acyclic graph (DAG) of data dependencies.

---

## 2. Retrospective Provenance (What Actually Happened)

Retrospective provenance captures **what actually ran**, on which inputs, and when.

Sources of retrospective provenance in this project:

- **Git history**  
  - All code and documentation are version-controlled in Git.  
  - Tags: `project-plan`, `status-report`, `final-project` mark key milestones.  

- **Snakemake logs**  
  - When the workflow is run, Snakemake prints execution logs, which can be
    redirected to a file if desired.  
  - Users can inspect which rules ran and whether any were re-executed.

- **Download log**  
  - `scripts/download_data.py` writes checksums and file sizes into
    `docs/provenance_download.log`.  
  - This log tracks which raw files were present and which may have been missing.

---

## 3. Provenance in the Report

In the final report (`README.md`):

- The **Reproducing** section references Snakemake as the canonical definition
  of the workflow and enumerates the steps to re-run it.  
- The **Data profile** and **Data quality** sections describe the origin of
  each dataset and the transformations applied.  

---

## 4. How to Extend Provenance

For future work, provenance could be strengthened by:

- Configuring Snakemake to write a `dag.png` of the workflow.  
- Saving Snakemake execution metadata (`.snakemake` directory) as part of the
  archival package.  
- Capturing environment hashes (e.g., conda env export) per run.
