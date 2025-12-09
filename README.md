# Mapping U.S. AI Data Centers Against Power Grid Capacity  
IS 477 Final Project Submission · Fall 2025

---

## Contributors  

- **Zhean Zhang** — data acquisition, integration pipeline architecture, workflow automation (Snakemake), figure generation, and primary report drafting  
- **Qichen Shen** — OSINT research and AI data center registry curation, renewable correlation analysis, result interpretation, metadata/documentation authoring, and reproduction testing  

Both contributors participated in design discussions, code review, data quality checks, and final polishing.

---

## Summary  

Large-scale artificial intelligence workloads are driving a new type of electric load that is both highly concentrated and rapidly growing. Modern GPU clusters for training and serving foundation models can require hundreds of megawatts per campus, and multiple campuses may be deployed within the same grid region. This raises several key questions for planners, regulators, and communities:  

1. Where are AI-oriented data centers being built in the United States?  
2. How do those siting decisions align with regional power grid capacity and fuel mix?  
3. Are there identifiable “stress zones” where AI load represents a high fraction of total capacity?  

This project addresses these questions by building an end-to-end, fully reproducible data pipeline that maps AI data centers against the U.S. power grid. The pipeline integrates three primary datasets:  

- **EPA eGRID 2023**, which provides subregional information about generation capacity, fuel mix (including renewable shares), and emissions intensity.  
- **EIA Form 860 (2024 snapshot)**, which describes generator-level capacity and fuel types across the U.S., allowing us to build region-level capacity baselines.  
- **An OSINT-based AI Data Center Registry**, curated from public sources and compiled into a structured CSV containing approximate locations and estimated AI power demand for more than 150 facilities.  

We adopt a clear and repeatable data lifecycle. Raw files are placed in `data/raw/`, transformed into cleaned/standardized forms in `data/interim/`, integrated into analysis-ready master tables in `data/processed/`, and finally summarized through visualizations stored in `results/figures/`. All steps are orchestrated by a single Snakemake workflow defined in `workflows/Snakefile`.  

The motivation is twofold. First, we want to demonstrate how standard data curation practices—cleaning, integration, quality assessment, and automation—can be applied to a timely, policy-relevant topic. Second, we aim to produce a workflow that someone else can rerun with minimal friction, satisfying reproducibility and transparency goals discussed in IS 477 (e.g., modules on workflows, provenance, and computational reproducibility).  

At a high level, our findings are:  

- AI data centers are not evenly distributed; they are heavily clustered in a few megaregions such as **Northern Virginia**, **Dallas–Fort Worth**, **Phoenix**, **Atlanta**, and **Central Oregon**.  
- When we compare estimated AI data center load (in MW) to regional capacity from eGRID/EIA, we identify roughly **20–25 subregions** where AI load reaches or exceeds a threshold (e.g., ≥15% of regional capacity), suggesting potential stress under continued growth.  
- The correlation between regional AI data center MW demand and renewable generation share is positive but modest, implying that siting is influenced by renewable potential but also by other factors such as land cost, transmission availability, cooling water resources, tax incentives, and fiber connectivity.  
- A simple timeline constructed from in-service or announcement years shows approximately **an order-of-magnitude increase** in AI-oriented data center count between 2016 and 2025.  

To support grading and reuse, we provide:  

- A complete repository with labeled directories (`data/`, `docs/`, `results/`, `scripts/`, `workflows/`).  
- Human-readable documentation (this `README.md`, a data dictionary, and project metadata).  
- A machine-executable workflow (Snakemake) and environment specifications (`environment.yml`, optional `requirements.txt`).  
- Box-hosted archives containing processed data and generated figures so that the TAs can inspect outputs without necessarily running the entire workflow.  

Together, these outputs form a reproducible package that can be extended to future data releases or adapted to similar infrastructure-versus-grid questions.

---

## Data Profile  

Our project uses three main datasets, plus additional documentation and metadata artifacts. This section describes each dataset in terms of content, structure, legal/ethical considerations, and role in the analysis.

### EPA eGRID 2023  

**Source & Content**  
The EPA eGRID dataset is a publicly available database describing power plant emissions, capacity, and fuel mix across the United States. For this project, we use the subregion-level tables that include:  

- Total generation and capacity for each eGRID subregion.  
- The fraction of generation from coal, gas, nuclear, hydro, wind, solar, and other sources.  
- CO₂ emissions rates (e.g., lb CO₂ per MWh of electricity generated).  

**Local Storage & Structure**  

- Raw file(s): `data/raw/egrid_2023.csv` (or similarly named eGRID extract).  
- After cleaning and standardization (e.g., normalizing region identifiers, pruning unused columns), a processed version is stored in `data/interim/egrid_clean.csv`.  

Key fields include a subregion identifier, state aggregation keys, capacity in MW, and fractions for major fuel categories.  

**Ethical and Legal Constraints**  

EPA eGRID is produced by a U.S. federal agency and is effectively public domain. There is no personally identifiable information, and it is explicitly intended for analytic and research use. We still cite it properly in `CITATIONS.md` and in the References section of this README.

**Role in Integration**  

eGRID supplies:  

- The denominator for some analyses (total regional capacity).  
- Measures of renewable and fossil intensity to which AI loads are compared.  
- Emissions factors that can be used to reason about marginal environmental impacts (qualitatively, in our case).

---

### EIA Form 860 (2024 snapshot)  

**Source & Content**  

EIA Form 860 is the primary generator- and plant-level registry of electricity assets in the U.S. It contains:  

- Plant codes and names.  
- Generator capacities, fuel types, and status (e.g., operating, proposed, retired).  
- Basic geographic information (state, sometimes latitude/longitude).  

**Local Storage & Structure**  

- Raw file: `data/raw/eia860_2024.csv` (or similar naming).  
- We aggregate capacity by region or subregion and save it to `data/interim/eia_agg.csv`.  

Important fields include:  

- `PLANT_CODE` or equivalent, which is used to group generators into plants.  
- `CAPACITY_MW` used in computing regional capacity sums.  
- `FUEL_TYPE` used to distinguish renewable vs fossil capacity shares.  

**Ethical and Legal Constraints**  

Like eGRID, EIA Form 860 is a public dataset and does not include individual-level information. It may be redistributed and reused as long as EIA is acknowledged.

**Role in Integration**  

Although eGRID alone provides some capacity information, using EIA 860 allows more control over how capacity is aggregated and categorized (e.g., by fuel). In our pipeline, EIA capacity is used to:  

- Validate capacity numbers coming from eGRID.  
- Provide a more detailed breakdown of renewable vs fossil capacity, when needed.  

This aggregated capacity then becomes a denominator when we calculate the percentage of regional capacity consumed by AI data centers.

---

### OSINT AI Data Center Registry  

**Source & Content**  

The OSINT AI Data Center Registry is a curated CSV created specifically for this project. It compiles information from:  

- Public press releases and infrastructure announcements by cloud providers and colocation companies.  
- Corporate sustainability and infrastructure reports.  
- News articles and public reporting on AI and hyperscale data center construction.  

The dataset includes more than 150 rows, each representing a facility (or campus) that is AI-relevant (e.g., GPU training sites, AI-focused expansions). Fields include:  

- Facility or campus name.  
- Provider/operator (e.g., AWS, Google, Meta, Microsoft, Nvidia, CoreWeave, etc.).  
- City and state.  
- Approximate latitude and longitude.  
- Estimated AI load in MW (`mw_estimated`).  
- Announcement or in-service year (`announced_year` or `in_service_year`).  

**Local Storage & Structure**  

- Raw file: `data/raw/osint_ai_centers_raw.csv`.  
- After cleaning (dropping rows without usable coordinates, correcting obvious typos), we write out `data/interim/osint_ai_cleaned.csv`.  

**Ethical and Legal Constraints**  

All entries originate from publicly visible content. We do not scrape or redistribute proprietary internal documents. Estimated MW values are **derived estimates** constructed to be reasonable based on ranges reported for similar facilities; they are not vendor-confirmed numbers and are documented as such.  

We do not include any data that could be considered personally identifiable or sensitive. Facilities are large industrial/commercial sites.

**Role in Integration**  

This registry is essential to the project because it defines “where the AI load is.” Without it, we would only know the grid side of the equation. Through integration, each facility is mapped to a grid region using its location, and its estimated MW is aggregated to compute regional AI demand.

---

### Metadata and Documentation  

In addition to the main datasets, the project includes:  

- `docs/data_dictionary.md` — a detailed listing of variables in the main processed tables (`integrated_master_dataset.csv` and `summary_regional_statistics.csv`), including definitions, units, allowed ranges, and notes on how each was constructed.  
- `docs/metadata_full.md` — a project-level metadata file that follows a DataCite/Schema.org style structure (title, creators, abstract, temporal coverage, geographic coverage, resource type, and license information).  
- `CITATIONS.md` — a list of formal citations for EPA, EIA, and other sources as appropriate.  

These documentation artifacts make the project more discoverable and reusable for future classes or research work.

---

## Data Quality  

Data quality is assessed and managed throughout the pipeline according to the principles discussed in IS 477. For this project, we focus on completeness, validity, accuracy (as far as feasible with public data), consistency, and reproducibility.

### Completeness  

We begin by assessing missing values in each dataset, especially for key analytical variables:

- In the OSINT registry, any facility that lacked both a usable location (city/state) and coordinates was deemed unusable and removed. For entries with city/state but missing coordinates, we used approximate latitude/longitude based on city centroids when possible. Remaining non-resolvable entries were dropped. This resulted in less than 2% of rows being excluded.  
- In eGRID and EIA, missing values in core capacity fields were rare. Rows with incomplete capacity or fuel data that could not be attributed to a region were either excluded or flagged and left out of capacity calculations, as documented in the cleaning logic.  

We summarize missingness and exclusions in the data dictionary and notes inside `docs/data_dictionary.md`.

### Validity  

Validity checks focus on whether values are plausible and fall within expected ranges:

- For the AI data center MW estimates, we treat any value below 20 MW or above 1500 MW as suspect. Values outside this range are reviewed, and if they cannot be justified (for example, unusually small test facilities that do not match the scope of this study), they are either removed or adjusted to a reasonable bound as described in the code.  
- For geographic coordinates, we validate that latitude and longitude fall within established bounds for the continental U.S. (or relevant territories) when used in U.S.-only analyses. Points outside these bounds are flagged and either corrected (if there is a clear typo) or excluded.  
- In EIA and eGRID, we perform type conversions and range checks for capacity fields to ensure that there are no negative or obviously corrupted values.  

### Accuracy  

We cannot fully verify the accuracy of every MW value in the OSINT registry, because they are often based on ranges described qualitatively (e.g., “up to 300 MW”) or announced in stages. However, we strive for reasonable accuracy by:

- Using publicly reported design capacities or ranges where available.  
- Cross-checking orders of magnitude against known typical values for hyperscale data centers and GPU clusters.  
- Comparing the resulting regional load distribution to external expectations (for instance, known major AI hubs such as Northern Virginia, Dallas–Fort Worth, etc.).  

Accuracy for eGRID and EIA is assumed based on their status as official datasets, though we still validate that simple derived statistics (e.g., total U.S. capacity) fall within published ballpark figures.

### Consistency  

We invest significant effort in harmonizing identifiers and categorical variables:

- State information is standardized to USPS two-letter codes (e.g., “VA” rather than “Virginia”).  
- Region identifiers are normalized to match across eGRID and EIA (where possible) so that lookups and joins behave consistently.  
- Facility names are cleaned to remove obvious duplicates (e.g., minor spelling variations or “DC” vs “Data Center”). Potential duplicates are combined when they appear to refer to the same physical campus.  

Consistency in these keys is essential for correct integration and aggregation.

### Provenance and Reproducibility  

One of the strongest aspects of data quality in this project is that **all transformation steps are encoded in code**. We do not manually edit intermediate CSV files in spreadsheet software. Instead:

- Cleaning steps for OSINT and EIA/eGRID data live in Python scripts and/or within the Snakemake rules in `workflows/Snakefile`.  
- Snakemake keeps track of which inputs generate which outputs, and logs are written under `.snakemake/`.  
- If the raw inputs are updated or changed, re-running the workflow regenerates all downstream products in a traceable way.  

This approach supports both internal quality control and external reproducibility.

---

## Findings  

The integrated dataset (`data/processed/integrated_master_dataset.csv`) and the associated summary statistics (`data/processed/summary_regional_statistics.csv`) form the basis of our analysis. We also generate a collection of visualizations in `results/figures/` that help communicate the findings.

### Geographic Concentration  

AI data centers are highly clustered in a small number of U.S. regions:

- **Northern Virginia (NOVA)** emerges as the single largest cluster, with dense AI capacity associated with hyperscale facilities.  
- **Dallas–Fort Worth (TX)** hosts multiple large-scale campuses leveraging a robust transmission network and business-friendly policies.  
- **Phoenix (AZ)** and surrounding areas show strong growth, partly driven by land availability and existing data center ecosystems.  
- **Atlanta (GA)** and **Central Oregon** (around The Dalles and Boardman) are also prominent clusters.  

These clusters are clearly visible in the choropleth and bubble maps (e.g., `fig1_choropleth.png`), which shade regions by total AI datacenter MW and mark individual facilities.

### Renewable Alignment  

We compute regional measures of renewable share using eGRID and compare them with AI datacenter MW. A simple correlation analysis yields a positive but moderate correlation coefficient (on the order of 0.3–0.4). This suggests:

- Regions with higher renewable shares do tend to attract some AI load, but  
- Many high-AI-load regions still rely substantially on fossil generation (e.g., gas-heavy areas).  

Scatterplots (such as `fig2_scatter_mw_vs_renewable.png`) reveal that there is significant variation: some renewable-rich areas host only modest AI capacity, while some fossil-heavy areas have large AI clusters.

### Grid Stress Indicators  

By dividing regional AI datacenter MW by total regional capacity, we obtain a rough “AI penetration percentage.” While this is a simplistic proxy (it does not model hourly dispatch, transmission constraints, or redundancy), it is still informative:

- We identify on the order of **20–25 regions** where the AI penetration exceeds a threshold such as 15%.  
- These regions may face particular challenges if AI loads grow faster than transmission and generation capacity can be expanded, particularly during peak conditions.  

Heatmaps (`fig3_heatmap.png`) and bar charts (`fig4_top10_power.png`) highlight which regions are most heavily impacted.

### Growth Over Time  

Using the announcement or in-service year field, we build a simple time series showing the cumulative count (and cumulative MW) of AI-oriented facilities. The curve is highly nonlinear, with relatively modest deployment prior to 2016 and rapid expansion from 2018 onward. By 2025, we see approximately an order-of-magnitude increase.  

The figure `fig6_timeseries_growth.png` shows this growth, indicating that AI infrastructure is expanding on a timescale that challenges traditional grid planning cycles.

---

## Future Work  

While this project demonstrates a functional and reproducible pipeline, it also highlights several directions for future work and improvements.

### More Detailed Power Modeling  

Our current approach uses annual or static capacity figures and approximate AI loads. Future work could:

- Incorporate hourly or seasonal load curves for both AI data centers and background demand.  
- Use models of power purchase agreements (PPAs), behind-the-meter renewable investments, and grid-scale batteries.  
- Distinguish between “nameplate capacity” and typical operating load, especially for facilities that are built in stages.  

This would allow more realistic stress tests and emissions estimates.

### Transmission and Congestion  

We treat each region as if it were a single “bucket” of capacity. In reality, constraints on transmission lines and substation capacity may limit the ability to move power to AI clusters. Future studies could:

- Integrate transmission network models and perform basic power flow or simplified congestion analyses.  
- Identify whether AI datacenters are predominantly located near transmission nodes with spare capacity or in already congested areas.  

### Policy and Incentive Analysis  

Siting decisions are influenced by tax incentives, land use policies, environmental regulations, and local politics. Future work could overlay:

- State and local tax incentive data.  
- Renewable portfolio standards (RPS) and clean energy targets.  
- Environmental permitting timeframes and local opposition indicators.  

This would help explain *why* certain regions attract more AI datacenters beyond pure grid characteristics.

### Environmental Justice and Equity  

Using tools such as EPA’s EJScreen or other demographic datasets, future work could examine whether AI datacenters—and their associated infrastructure—are disproportionately sited in or near communities that already face higher pollution or socioeconomic burdens. This would be important for understanding potential equity implications of AI infrastructure build-out.

### International Extension  

Our current study focuses on the U.S., largely because eGRID and EIA provide standardized, detailed data. Extending to Europe, Asia, or other regions would require incorporating international datasets (e.g., ENTSO-E data, IEA statistics) and adapting the integration logic. However, the same pipeline pattern (raw → interim → processed → figures) and workflow tooling (Snakemake) are reusable.

---

## Reproducing  

This section describes how another person can reproduce our analysis or at least inspect the results.

### Option A: Use Box Outputs (No Workflow Execution Required)  

We provide Box folders containing the final processed datasets and figures. To use this option:

1. Clone the repository or download it from GitHub:

   ```bash
   git clone https://github.com/jimmy0303/is477project
   cd is477project
2. Download and extract the Box folders as follows:

   | Box Link | Destination Folder |
   |---|---|
   | https://uofi.box.com/s/7orbrt914w7ieqjew6a1zi39kbs02cl8 | `./data/processed/` |
   | https://uofi.box.com/s/jh30p92t27jgblbtnh1ihk2kvppxsfkd | `./results/figures/` |
   | https://uofi.box.com/s/qzoqq896hsmwii614wod16yru5v6e4nn | project root (contains a full output bundle) |

3. After extraction, you should be able to open  
   - `data/processed/integrated_master_dataset.csv`  
   - `data/processed/summary_regional_statistics.csv`  
   - and all PNG figures under `results/figures/`  
   without running any code.  
   This is the fastest evaluation path for grading.

---

### Option B: Full Workflow Execution

If you wish to reproduce the entire project from raw source files:

```bash
git clone https://github.com/jimmy0303/is477project
cd is477project
conda env create -f environment.yml
conda activate ai-grid-project
