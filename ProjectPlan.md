# ProjectPlan.md

## 1. Overview

Artificial Intelligence (AI) infrastructure is expanding rapidly across the United States. Major cloud providers and specialized AI companies are building large-scale data centers that require significant electrical power—often in regions with limited grid capacity. This rapid growth raises critical questions about whether **local power grids can support the scale of AI infrastructure**, and whether data center development is aligned with **renewable energy availability** and **decarbonization goals**.

This project integrates **public power grid data** (EPA eGRID and EIA capacity datasets) with **OSINT-based data center location data** to analyze **the geographic alignment between AI data center growth and regional energy capacity**. By combining structured government datasets with semi-structured OSINT data, we aim to build an automated, reproducible geospatial analysis pipeline that follows the full **data lifecycle** and meets the ethical, technical, and documentation standards of this course.

---

## 2. Research Questions

1. Where are AI data centers being built in the U.S., and how does their distribution compare to regional power grid capacity?
2. Is there a geographic correlation between AI data center concentration and renewable energy share?
3. Are there regions where data center expansion is outpacing local grid capacity, indicating future infrastructure stress?

---

## 3. Team Roles and Responsibilities

| Name            | Role                              | Responsibilities                                                                                                                                                                                                 |
| --------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Zhean Zhang** | Data Engineer / OSINT Lead        | Collect OSINT data on AI data centers, implement geocoding, set up automated pipelines for EIA/eGRID APIs, integrate datasets using Pandas/SQL, build Snakemake workflow, conduct analysis and visualization     |
| **Qichen Shen** | Data Curator / Documentation Lead | Clean and normalize OSINT datasets, ensure ethical and legal compliance, manage metadata and codebooks, conduct data profiling and quality assessments, write documentation for reproducibility and transparency |

**Collaboration and GitHub:**

* All work will be tracked in a shared GitHub repository.
* Each member will use separate branches and pull requests.
* Contributions will be visible in commit history.
* Major deliverables will be tagged with version releases (`project-plan`, `status-report`, `final-project`).

---

## 4. Datasets

### 4.1 EPA eGRID 2023

* **Source:** [EPA eGRID](https://www.epa.gov/egrid)
* **Format:** XLSX
* **Content:** Regional electricity generation, resource mix, emissions, plant attributes.
* **Use:** Identify regional power capacity and renewable energy availability.
* **Ethical/Legal:** Public domain; attribution required.

### 4.2 EIA Form 860 (2024)

* **Source:** [EIA Form 860](https://www.eia.gov/electricity/data/eia860/)
* **Format:** CSV
* **Content:** Generator capacity (MW), energy source, location.
* **Use:** Quantify grid capacity near data centers.
* **Ethical/Legal:** Public domain.

### 4.3 OSINT AI Data Center Locations

* **Source:** Business Insider investigation, DataCenterMap, company press releases.
* **Format:** Custom CSV compiled by team.
* **Fields:** Company, site name, address, state, coordinates, year announced, estimated power capacity.
* **Use:** Identify AI data center locations and integrate with grid data via spatial joins.
* **Ethical/Legal:** Public sources only; no scraping behind logins; all citations included.

---

## 5. Timeline

| Task                     | Description                              | Lead           | Due       |
| ------------------------ | ---------------------------------------- | -------------- | --------- |
| Team setup & repo        | Canvas group + GitHub repo creation      | Both           | Sept 26   |
| Project plan             | Draft, commit, tag `project-plan`        | Both           | Oct 7     |
| Data collection          | OSINT (AI centers) + EIA/eGRID           | Zhean          | Oct 20–25 |
| Storage & integration    | Repo structure, DB schema, spatial joins | Both           | Nov 1     |
| Quality & workflow       | Data cleaning, Snakemake automation      | Qichen & Zhean | Nov 5–10  |
| Interim status report    | Progress update, tag `status-report`     | Both           | Nov 11    |
| Analysis & visualization | Correlation & mapping                    | Both           | Nov 25    |
| Documentation & final    | Metadata, reproducibility, release       | Both           | Dec 1–10  |

---

## 6. Constraints

* OSINT data may be incomplete or ambiguous; some sites may lack MW capacity data.
* Geospatial alignment between OSINT and grid regions may require fuzzy matching.
* EIA API rate limits may require caching.
* Energy data is annual; OSINT data may be at project-phase level.

---

## 7. Gaps and Areas for Input

* Finalize inclusion criteria for “AI data center.”
* Decide how to handle missing capacity values.
* Choose best visualization formats (e.g., state vs. county choropleths).

---

## 8. Data Lifecycle Alignment

We follow the **Plan → Collect → Integrate → Analyze → Preserve → Reuse** model:

* **Plan:** Defined research questions and sources.
* **Collect:** Use APIs, OSINT, downloads with checksums.
* **Integrate:** Spatial joins via coordinates and FIPS codes.
* **Analyze:** Correlate capacity with data center presence.
* **Preserve:** Version control + metadata.
* **Reuse:** Document in README and automate with workflows.

---

## 9. Ethical, Legal, and Policy Considerations

* All datasets are public domain or publicly disclosed OSINT.
* No personal or proprietary information collected.
* OSINT will be verified and cited properly.
* All licenses and terms of use will be followed.

---

## 10. Anticipation of Later Topics

| Requirement              | How Addressed                                     |
| ------------------------ | ------------------------------------------------- |
| Extraction & Enrichment  | Geocoding, renewable energy share                 |
| Integration              | Spatial joins between datasets                    |
| Data Quality & Cleaning  | Profiling, standardization, fixing missing fields |
| Workflow Automation      | Snakemake + run-all scripts                       |
| Reproducibility          | Documented steps, metadata, version control       |
| Metadata & Documentation | Codebook, README, Schema.org/DataCite             |
| Licensing & Citation     | LICENSE file + citations in final README          |

---

## 11. Reproducibility Notes

* All data and scripts will be stored under version control.
* Large inputs will be hosted on Box with links in README.
* A `requirements.txt` will list Python dependencies.
* Optional Dockerfile may be included for full environment capture.
