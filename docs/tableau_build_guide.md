# Tableau Build & Architecture Guide

**Project:** EV Market Analysis  
**Student:** Nipun Jain  
**Workbook:** `tableau/EV Market Analysis.twbx` (100,000 records)  
**Tableau Story:** [View on Tableau Public](https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)

---

## 1. Connecting Data
1. Open Tableau Desktop / Tableau Public.
2. Select **Connect to Data > Text File** (for `data/raw/ev_market_test.csv`) or **MySQL** (for database view `vw_ev_clean`).
3. Set connection mode to **Extract** to optimize performance for 100,000 records.

---

## 2. Calculated Fields & Logic
| Field Name | Formula | Description |
|---|---|---|
| **Range per $1000** | `[range_km] / [price_usd] * 1000` | Efficiency metric: kilometers of driving range per $1,000 vehicle cost |
| **Price Segment** | `IF [price_usd] < 20000 THEN "Budget" ELSEIF [price_usd] < 60000 THEN "Mid-range" ELSEIF [price_usd] < 120000 THEN "Premium" ELSE "Luxury" END` | 4-tier price grouping |
| **Range Class** | `IF [range_km] >= 450 THEN "Long" ELSEIF [range_km] >= 250 THEN "Medium" ELSE "Short" END` | 3-tier driving range classification |
| **Fast Charge Rating** | `IF [charging_dc_fast_time_min] <= 15 THEN "Ultra-fast" ELSEIF [charging_dc_fast_time_min] <= 25 THEN "Fast" ELSE "Standard" END` | DC fast-charging benchmark |
| **Revenue (Est.)** | `[price_usd] * [annual_sales_units]` | Gross revenue proxy |
| **Sales Share %** | `SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))` | Category / manufacturer volume contribution |
| **Is Top N** | `RANK(SUM([annual_sales_units])) <= [Top N Manufacturers]` | Dynamic rank filter driven by parameter |

---

## 3. Worksheets Implementation Summary
1. **Sales by Category:** Bar chart ranking 15 vehicle categories by summed `annual_sales_units`.
2. **Sales by Year:** Line chart showing annual sales trends across 2018–2026.
3. **Top Manufacturers:** Dynamic bar chart filtered by `Is Top N` parameter (default 10 of 200).
4. **Country Map:** Filled geographic map encoding manufacturing locations by production volume.
5. **Region Price:** Bar chart displaying average `price_usd` across 7 global market regions.
6. **Battery Share:** Donut / Pie chart illustrating market share of 5 battery chemistries.
7. **Battery Durability:** Dual-axis chart comparing `battery_cycle_life` against `battery_degradation_pct_5yr`.
8. **Price vs Range:** Scatter plot categorized by vehicle class with trend lines.
9. **Drivetrain Heatmap:** Two-dimensional matrix of Category vs Drivetrain (FWD, RWD, AWD).
10. **Use Case:** Treemap representing distribution across 7 recommended operational use cases.
11. **CO2 Saved:** Stacked bar chart showing annual metric tons of CO₂ saved by category and region.
12. **Rating Histogram:** Continuous distribution of `customer_rating` (1.0 to 5.0 stars).

---

## 4. Dashboard Assembly
- **Market Overview:** Integrates executive KPIs, Category Sales, Yearly Trends, Top Manufacturers, and Regional Pricing.
- **Technology:** Integrates Battery Share, Durability, Price vs Range, and Drivetrain Heatmap.
- **Geography and Impact:** Integrates Country Map, Recommended Use Case, CO₂ Savings, and Rating Histogram.
- **Sizing:** Set to Automatic with Device Designer profiles for Desktop, Tablet, and Mobile.

---

## 5. Story Point Narrative (6 Scenes)
1. **Market Snapshot:** 100,000 models, $65,010 average price, 324 km average range.
2. **Who Sells the Most:** Scooters, Sedans, and Compact SUVs drive mass volume.
3. **Price vs Range:** Strong battery capacity correlation (0.84) versus moderate range correlation (0.28).
4. **Battery Technology:** Solid-State and LFP deliver highest longevity and lowest degradation.
5. **Regions & Countries:** Balanced international adoption across Asia, Europe, and North America.
6. **Recommendations:** Strategic focus on high-efficiency urban transport and next-gen battery chemistries.
