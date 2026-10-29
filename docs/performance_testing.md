# Performance Testing & Optimization Report

**Project:** EV Market Analysis  
**Student Name:** Nipun Jain  
**Environment:** Tableau Public / MySQL & SQLite / Python 3  
**Dataset:** `data/raw/ev_market_test.csv` (100,000 records)  

---

## 1. Amount of Data Rendered
- **Total Records Rendered:** Exactly **100,000 rows** (EV models / variants from 2018 to 2026).
- **Attribute Width:** **37 original columns** + **5 derived analytical dimensions**.
- **Data Volume:** 23.2 MB raw CSV, 36.3 MB indexed relational database (`ev_market.db`), and 8.3 MB packaged Hyper extract.
- **Connection Optimization (Live vs. Extract):**
  - **Live Database Connection:** Query execution took ~2.8 to 4.2 seconds across full-table group-by aggregations.
  - **Tableau Hyper Extract (`.twbx`):** Render latency dropped to **< 0.8 seconds**, enabling instant client-side cross-filtering and responsive dashboard interactivity across all 100,000 records without dropping rows.

---

## 2. Utilization of Filters
To balance high analytical granularity with fast UI responsiveness, **6 synchronized global filters** were implemented:
1. **`model_year`:** Continuous range slider (2018–2026) allowing year-by-year temporal slicing.
2. **`market_region`:** Multi-select checklist for the 7 geographic markets (North America, Europe, Asia Pacific, Latin America, Middle East, Africa, South Asia).
3. **`category`:** Multi-select dropdown filtering across 15 vehicle categories.
4. **`battery_type`:** Single-select dropdown targeting specific battery chemistries (NMC, LFP, NCA, Sodium-Ion, Solid-State).
5. **`Price Segment`:** Categorical checklist (Budget, Mid-range, Premium, Luxury).
6. **`Top N Manufacturers`:** Dynamic integer parameter (range 5 to 30, default 10) driving the `Is Top N` rank calculation.
- **Filter Scope:** All 6 filters are set to **"All Using This Data Source"**, ensuring synchronized multi-worksheet cross-filtering while sharing a single cached query context.

---

## 3. Number of Calculated Fields
A total of **6 core business metrics** + **1 dynamic ranking filter** + **1 user parameter** were engineered:
1. **`Range per $1000`**:
   ```tableau
   [range_km] / [price_usd] * 1000
   ```
   *Measures capital efficiency: driving kilometers gained per $1,000 vehicle cost.*
2. **`Price Segment`**:
   ```tableau
   IF [price_usd] < 20000 THEN "Budget"
   ELSEIF [price_usd] < 60000 THEN "Mid-range"
   ELSEIF [price_usd] < 120000 THEN "Premium"
   ELSE "Luxury" END
   ```
   *Groups vehicles into 4 standard economic price bands.*
3. **`Range Class`**:
   ```tableau
   IF [range_km] >= 450 THEN "Long"
   ELSEIF [range_km] >= 250 THEN "Medium"
   ELSE "Short" END
   ```
   *Segments vehicles into Short (<250 km), Medium (250–449 km), and Long (>=450 km).*
4. **`Fast Charge Rating`**:
   ```tableau
   IF [charging_dc_fast_time_min] <= 15 THEN "Ultra-fast"
   ELSEIF [charging_dc_fast_time_min] <= 25 THEN "Fast"
   ELSE "Standard" END
   ```
   *Categorizes DC fast-charging velocity.*
5. **`Revenue (Est.)`**:
   ```tableau
   [price_usd] * [annual_sales_units]
   ```
   *Model-level gross commercial revenue proxy.*
6. **`Sales Share %`**:
   ```tableau
   SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))
   ```
   *Percentage contribution of a category or brand to total sales.*
7. **`Is Top N`** (Dynamic Rank Filter):
   ```tableau
   RANK(SUM([annual_sales_units])) <= [Top N Manufacturers]
   ```
   *Restricts mark generation to only top volume leaders, eliminating DOM bloat.*
8. **Parameter `Top N Manufacturers`**: Integer range [5, 30], default value = 10.

---

## 4. Number of Visualizations / Graphs
Exactly **12 dedicated visualizations** were constructed and validated across 3 coordinated dashboards:
1. **Sales by Category:** Horizontal bar chart displaying volume leaders across all 15 vehicle categories.
2. **Sales by Year:** Line chart illustrating historical volume trends from 2018 to 2026.
3. **Top Manufacturers:** Ranked bar chart dynamically filtered by the `Top N Manufacturers` parameter.
4. **Country Map:** Filled geographic map displaying global manufacturing facility locations.
5. **Region Price:** Bar chart analyzing average vehicle acquisition cost across the 7 market regions.
6. **Battery Share:** Donut / Pie chart visualizing market share across 5 battery chemistries.
7. **Battery Durability:** Dual-axis chart benchmarking cycle life (up to 2,999 cycles) against 5-year degradation rate.
8. **Price vs Range:** Scatter plot categorized by vehicle class demonstrating battery pack cost correlation.
9. **Drivetrain Heatmap:** Density matrix crossing vehicle categories against FWD, RWD, and AWD architectures.
10. **Use Case:** Treemap representing fleet distribution across 7 recommended operational use cases.
11. **CO2 Saved:** Stacked bar chart quantifying annual greenhouse gas displacement by category and region.
12. **Rating Histogram:** Distribution histogram of customer satisfaction ratings (1.0 to 5.0 stars).

---

## 5. Performance Summary Table

| Metric | Measured Specification |
|---|---|
| **Underlying Records Rendered** | 100,000 rows |
| **Attribute Width** | 37 original columns + 5 derived fields |
| **Global Data Filters** | 6 synchronized filters + 1 dynamic parameter |
| **Calculated Fields** | 6 metrics + 1 rank field + 1 parameter |
| **Visualizations Built** | 12 dedicated worksheets |
| **Dashboards / Story Points** | 3 coordinated dashboards / 6 narrative scenes |
| **Extract Filter Latency** | < 0.8 seconds |
