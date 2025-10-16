# ProjectPlan.md

## 1. Overview

Artificial Intelligence (AI) infrastructure is expanding rapidly across the United States. Major cloud providers and specialized AI companies are building large-scale data centers that require significant electrical power—often in regions with limited grid capacity. This rapid growth raises critical questions about whether **local power grids can support the scale of AI infrastructure**, and whether data center development is aligned with **renewable energy availability** and **decarbonization goals**.

This project will integrate **public power grid data** (EPA eGRID and EIA capacity datasets) with **OSINT-based data center location data** to analyze **the geographic alignment between AI data center growth and regional energy capacity**. By combining structured government datasets with semi-structured OSINT data, we aim to create an automated, reproducible geospatial analysis pipeline that follows the full **data lifecycle** and meets the ethical, technical, and documentation standards of this course.

---

## 2. Research Questions

1. **Where are AI data centers being built in the U.S., and how does their distribution compare to regional power grid capacity?**
2. **Is there a geographic correlation between AI data center concentration and renewable energy share?**
3. **Are there regions where data center expansion is outpacing local grid capacity, indicating future infrastructure stress?**

---

## 3. Team Roles and Responsibilities

| Name            | Role                              | Responsibilities                                                                                                                                                                                                            |
| --------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Zhean Zhang** | Data Engineer / OSINT Lead        | Collect OSINT data on AI data centers, implement geocoding, set up automated pipelines for EIA/eGRID APIs, integrate datasets using Pandas/SQL, build Snakemake workflow, conduct exploratory analysis and visualization    |
| **Qichen Shen** | Data Curator / Documentation Lead | Clean and normalize OSINT datasets, ensure ethical and legal compliance of sources, manage metadata and codebooks, conduct data profiling and quality assessments, write documentation for reproducibility and transparency |

**Collaboration and GitHub:**

* All work will be tracked in a shared GitHub repository.
* Each member will use separate branches and pull requests for merging.
* Contributions will be visible in Git commit history.
* Major deliverables will be tagged with version releases (`project-plan`, `status-report`, `final-project`).

---

## 4. Datasets

### 4.1 EPA eGRID 2023

* **Source:** [EPA eGRID](https://www.epa.gov/egrid)
* **Format:** XLSX (download)
* **Content:** Regional electricity generation, resource mix (renewable vs. non-renewable), emissions, balancing authority codes, plant attributes.
* **Use:** Identify regional power capacity and renewable energy availability for counties/states containing data centers.
* **Ethical/Legal:** Public domain U.S. federal dataset. Attribution required.

### 4.2 EIA Form 860 (2024 Final Release)

* **Source:** [EIA Form 860 Data](https://www.eia.gov/electricity/data/eia860/)
* **Format:** CSV
* **Content:** Generator-level nameplate capacity (MW), primary energy source, plant location, operational status.
* **Use:** Quantify actual grid capacity near data centers.
* **Ethical/Legal:** Public domain.

### 4.3 OSINT AI Data Center Locations

* **Source:** Business Insider data center investigation table, DataCenterMap, company press releases (e.g., Applied Digital, Meta, Amazon, Microsoft, EdgeConneX).
* **Format:** Custom CSV compiled by team.
* **Fields:** Company, site name, street address, state, latitude/longitude (via geocoding), year announced, estimated power capacity (if disclosed).
* **Use:** Identify locations of AI data centers and link them to eGRID/EIA regions through geospatial joins.
* **Ethical/Legal:** Only publicly disclosed information will be used. All sources will be cited. No private or scraped-behind-login data.

---

## 5. Timeline

| Task                        | Description                            | Lead   | Due Date    |
| --------------------------- | -------------------------------------- | ------ | ----------- |
| Team Formation & Repo Setup | Canvas group, GitHub repo              | Both   | **Sept 26** |
| Project Plan                | Draft, commit, tag `project-plan`      | Both   | **Oct 7**   |
| OSINT Collection & Cleaning | Compile data center list, geocode      | Zhean  | **Oct 20**  |
| EIA/eGRID Acquisition       | Pull via API/download, clean           | Zhean  | **Oct 25**  |
| Storage & Organization      | Directory structure, SQLite schema     | Zhean  | **Oct 28**  |
| Integration                 | Spatial joins (FIPS/coordinates)       | Both   | **Nov 1**   |
| Data Quality Assessment     | Profiling, missing data, validation    | Qichen | **Nov 5**   |
| Workflow Automation         | Snakemake + run-all scripts            | Zhean  | **Nov 10**  |
| Interim Status Report       | Commit, tag `status-report`            | Both   | **Nov 11**  |
| Analysis & Visualization    | Choropleth maps, correlation           | Both   | **Nov 25**  |
| Documentation & Metadata    | Codebook, reproducibility instructions | Qichen | **Dec 1**   |
| Final Submission            | Tag `final-project`, release           | Both   | **Dec 10**  |

---

## 6. Constraints

* OSINT data may be incomplete or ambiguous; some sites may not disclose exact MW capacity.
* Geospatial alignment between OSINT and grid regions may require fuzzy matching.
* API rate limits (EIA) may require local caching.
* Energy datasets use annual resolution, while OSINT announcements may be at monthly or project-phase level.

---

## 7. Gaps and Areas for Input

* Finalize inclusion criteria for “AI data center” vs. generic data center.
* Determine how to handle missing capacity data (e.g., imputation or exclusion).
* Decide the best visualization format for the final analysis (state-level choropleths vs. county-level scatterplots).

---

## 8. Data Lifecycle Alignment

We follow the **Plan → Collect → Integrate → Analyze → Preserve → Reuse** model:

* **Plan:** Defined questions and sources.
* **Collect:** Use APIs, OSINT scraping, and downloads with checksums.
* **Integrate:** Spatial join via coordinates and FIPS codes.
* **Analyze:** Correlation between capacity and AI data center presence.
* **Preserve:** Store datasets with metadata and version control.
* **Reuse:** Document in README and publish reproducible workflow.

---

## 9. Ethical, Legal, and Policy Considerations

* All datasets are either U.S. federal public domain or public OSINT sources.
* No private, personal, or proprietary information will be collected.
* OSINT will be verified and attributed; scraping will be limited to publicly accessible pages without authentication.
* All data will be cited in the final report, and licenses respected.

---

## 10. Anticipation of Later Topics

| Requirement                  | How Addressed                                                           |
| ---------------------------- | ----------------------------------------------------------------------- |
| **Extraction & Enrichment**  | Geocoding of OSINT addresses; adding renewable share from eGRID         |
| **Integration**              | Spatial joins between datasets                                          |
| **Data Quality**             | Profiling completeness and consistency                                  |
| **Cleaning**                 | Remove duplicates, standardize coordinate formats, fix missing fields   |
| **Workflow Automation**      | Snakemake pipeline and run-all script                                   |
| **Reproducibility**          | Documented steps + code + metadata in repo                              |
| **Metadata & Documentation** | Data dictionary, README, descriptive metadata using Schema.org/DataCite |
| **Licensing & Citation**     | Include LICENSE file and citations in final README                      |

---

## 11. Constraints & Reproducibility Notes

* All data and scripts will be stored in GitHub under version control.
* Large input datasets will be hosted on Box, with access links in the README.
* A `requirements.txt` will list all Python dependencies.
* Optional Dockerfile may be added for complete environment reproducibility.
