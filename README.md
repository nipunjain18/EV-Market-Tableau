# Global Electric Vehicle Market Analysis

**Author:** Nipun Jain  
**Domain:** Data Analytics and Business Intelligence  
**Tools & Technologies:** Tableau Public, Python (Flask, pandas), SQL (SQLite / MySQL), HTML5/CSS3, Git, GitHub  

---

## Project Overview

The Electric Vehicle (EV) market is undergoing explosive growth globally, characterized by shifts in battery chemistry, divergent regional preferences, and evolving consumer use cases. This end-to-end data analytics project provides comprehensive market intelligence by evaluating **100,000 EV models** across **37 technical and commercial parameters** spanning model years **2018 through 2026**.

The project implements a complete Business Intelligence pipeline:
1. **Data Ingestion & Integrity Auditing:** Preserving the verified 100,000-record reference dataset (`ev_market_test.csv`).
2. **Relational Database Storage:** Managing data in SQLite (`data/ev_market.db`) and MySQL with custom performance indexing.
3. **Advanced SQL Querying:** Executing 10 multi-dimensional analytical queries to extract commercial and engineering benchmarks.
4. **Interactive Tableau BI:** Building 12 worksheets, 3 responsive dashboards, and a 6-scene structured narrative Story.
5. **Web Portal Deployment:** Embedding interactive Tableau Public views inside a modern, responsive Flask web application.

---

## Live Links & Deliverables

- **Published Tableau Story:** [Tableau Public Story — Nipun Jain](https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)
- **Published Tableau Dashboard:** [Tableau Public Market Overview](https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview)
- **Project Report:** `EV_Market_Tableau_Project_Report.pdf` (Included in root and `docs/`)
- **Packaged Tableau Workbook:** `tableau/EV Market Analysis.twbx` (Preserved 15.3 MB workbook with embedded extract)

---

## Verified Dataset Specifications

> **Important Data Fidelity Note:**  
> This project strictly utilizes the primary reference dataset embedded within the Tableau workbook (`ev_market_test.csv`). The dataset contains exactly **100,000 records** and **37 columns**. It does **not** use the separate 199,999-row `ev_market_cleaned.csv` dataset, ensuring 100% data consistency between the SQL analysis, documentation, and the published Tableau Public Story.

- **Total Records:** 100,000 EV models / variants
- **Total Columns:** 37 attributes (Categorized across Vehicle Identity, Battery Technology, Driving Performance, Charging, Physical Specifications, Commercial Economics, and Environmental Impact)
- **Model Years:** 2018 to 2026
- **Unique Manufacturers:** 200 distinct global automotive brands
- **Unique Vehicle Categories:** 15 classes (from Two-Wheeler Scooters to Commercial Buses and Heavy Trucks)
- **Average Fleet Price:** \$65,010.46 (Min: \$900.04, Max: \$409,995.49)
- **Average Fleet Range:** 324.31 km (Min: 55.0 km, Max: 659.9 km)
- **Total Annual Sales Units (Synthetic):** 772,608,124 units

---

## Repository Structure

```
EV-Market-Tableau/
├── .env.example                     # Environment configuration template
├── .env                             # Local environment settings (pre-configured)
├── .gitignore                       # Git ignore rules
├── app.py                           # Flask web server embedding Tableau API
├── requirements.txt                 # Python package requirements
├── README.md                        # Complete project documentation
├── EV_Market_Tableau_Project_Report.pdf # Final PDF Report
├── data/
│   ├── raw/
│   │   └── ev_market_test.csv       # Preserved 100,000-record reference dataset
│   ├── cleaned/
│   │   └── ev_market_clean.csv      # Cleaned dataset with derived calculated fields
│   └── ev_market.db                 # SQLite database loaded with 100k rows
├── scripts/
│   ├── load_to_db.py                # Database loader script (SQLite / MySQL)
│   └── clean_data.py                # Data transformation & feature derivation script
├── sql/
│   ├── schema.sql                   # DDL table creation and indexing statements
│   └── queries.sql                  # 10 verified analytical SQL queries
├── tableau/
│   ├── EV Market Analysis.twbx      # Preserved Tableau packaged workbook
│   └── README.md                    # Detailed Tableau worksheet & dashboard guide
├── templates/                       # Flask Jinja2 HTML templates
│   ├── base.html                    # Base layout with navigation and branding
│   ├── index.html                   # Project landing page and summary
│   ├── dashboard.html               # Interactive Dashboard embed page
│   ├── story.html                   # 6-scene Tableau Story embed page
│   ├── about.html                   # Project metadata and student information
│   └── embed.html                   # Reusable Tableau Embedding API v3 component
├── static/
│   └── css/
│       └── style.css                # Responsive stylesheet with light/dark theme
└── docs/
    ├── EV_Market_Tableau_Project_Report.pdf # Project report copy
    ├── tableau_build_guide.md       # Step-by-step Tableau worksheet build guide
    ├── performance_testing.md       # Benchmark and optimization documentation
    ├── charts/                      # Visualization PNG charts
    └── screenshots/                 # Database, SQL, and Web UI screenshots
```

---

## Tableau Worksheets, Dashboards & Story

### 12 Worksheets
1. **Sales by Category:** Bar chart ranking volume leaders (Scooters lead with 85.0M units).
2. **Sales by Model Year:** Line chart showing temporal volume distribution (2018–2026).
3. **Top N Manufacturers:** Dynamic bar chart filtered by dynamic ranking parameter (Top 10 of 200).
4. **Manufacturing Country Map:** Geographic filled map highlighting vehicle manufacturing centers.
5. **Region vs Average Price:** Regional pricing comparison across 7 global markets.
6. **Battery Type Share:** Donut / Pie visualization displaying market breakdown of 5 chemistries.
7. **Battery Durability:** Dual-axis chart comparing cycle life (up to 2,999 cycles) vs 5-year degradation (7.36%–14.02%).
8. **Price vs Driving Range:** Scatter plot categorized by class illustrating battery cost dynamics.
9. **Category and Drivetrain Heatmap:** Density matrix of FWD, RWD, and AWD architectures.
10. **Recommended Use Case:** Treemap categorizing operational suitability.
11. **CO₂ Savings:** Stacked bar chart calculating environmental greenhouse gas displacement.
12. **Customer Rating Distribution:** Continuous histogram of customer satisfaction ratings.

### 3 Interactive Dashboards
- **Market Overview:** Executive KPI summary, Category Sales, Yearly Trends, Top Manufacturers, Regional Pricing.
- **Technology:** Battery chemistry comparison, Durability benchmarks, Price vs Range scatter, Drivetrain heatmap.
- **Geography and Impact:** Global manufacturing map, Operational use cases, CO₂ offsets, Rating distribution.

### 6-Scene Narrative Story
1. **Market Snapshot:** Fleet scale and baseline metrics (100k models, \$65k avg price, 324 km avg range).
2. **Who Sells the Most:** Mass adoption concentrated in urban transit (Scooters, Sedans, Compact SUVs).
3. **Price vs Range:** Empirical demonstration that battery capacity (r=0.84), not range (r=0.28), drives price.
4. **Battery Technology:** Solid-State and LFP chemistries proven as longevity leaders.
5. **Regions & Countries:** Balanced global manufacturing footprint.
6. **Recommendations:** Strategic transition toward high-efficiency urban platforms and durable chemistries.

---

## Quickstart & Execution Guide

### Prerequisites
- Python 3.9+ (Python 3.10–3.14 fully supported)
- Tableau Public or Tableau Desktop
- SQLite (included with Python) or optional MySQL 8.0+

### Setup Steps
```bash
# 1. Clone repository and navigate to directory
git clone https://github.com/nipun-jain/ev-market-tableau.git
cd EV-Market-Tableau

# 2. Set up virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate          # On Windows (macOS/Linux: source venv/bin/activate)
python -m pip install -r requirements.txt

# 3. Process data and generate derived features
python scripts/clean_data.py

# 4. Load dataset into database (Loads 100,000 rows into data/ev_market.db)
python scripts/load_to_db.py

# 5. Start the Flask Web Portal
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to view the interactive portal.

---

## Academic Integrity & Attribution

- **Student Author:** Nipun Jain
- **Academic Context:** Data Analytics and Business Intelligence Project
- **Attribution:** The architectural foundation and Tableau visualization designs for this project were adapted from a peer reference implementation. The data pipeline, database loader, SQL queries, calculations, web application, and report have been audited, verified against the 100,000-record reference dataset, and customized for Nipun Jain.
