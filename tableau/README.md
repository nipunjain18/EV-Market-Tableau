# Tableau Workbook Architecture — EV Market Analysis

**Author:** Nipun Jain  
**Workbook File:** `EV Market Analysis.twbx` (15.3 MB packaged workbook with embedded extract)  
**Published Tableau Story:** [Tableau Public Story](https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)  
**Published Dashboard:** [Tableau Public Market Overview](https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview)

---

## 1. Verified Data Source and Connection
- **Data Source Name:** `ev_market_test.csv` (Federated extract: `federated_1wvw2m11oqn5wt1emokjp1.hyper`)
- **Total Record Count:** Exactly 100,000 records (no records dropped or substituted)
- **Total Attributes:** 37 base dimensions & measures
- **Connection Mode:** Packaged Extract (`.twbx`), retaining zero external runtime dependencies.

---

## 2. Worksheets (12 Preserved Sheets)

| # | Worksheet Name | Chart Type | Core Question Answered |
|---|---|---|---|
| 1 | **Sales by Category** | Horizontal Bar Chart | Which vehicle categories lead in annual sales volume? |
| 2 | **Sales by Year** | Trend Line Chart | How have sales evolved over model years (2018–2026)? |
| 3 | **Top Manufacturers** | Ranked Bar Chart | Which manufacturers dominate sales (filtered via Top N)? |
| 4 | **Country Map** | Filled Geographic Map | Where are EV manufacturing facilities concentrated globally? |
| 5 | **Region Price** | Categorical Bar Chart | How does average vehicle price vary across the 7 market regions? |
| 6 | **Battery Share** | Donut / Pie Chart | What is the market share distribution of the 5 battery chemistries? |
| 7 | **Battery Durability** | Dual-Axis Bar / Point Chart | Which battery chemistries offer highest cycle life & lowest degradation? |
| 8 | **Price vs Range** | Scatter Plot by Category | What is the relationship between price and range across vehicle classes? |
| 9 | **Drivetrain Heatmap** | Matrix Heatmap | How do FWD, RWD, and AWD drivetrains distribute across categories? |
| 10 | **Use Case** | Treemap | How are EV models categorized by intended operational use cases? |
| 11 | **CO2 Saved** | Stacked Bar Chart | Which vehicle categories and regions drive the greatest CO₂ savings? |
| 12 | **Rating Histogram** | Distribution Histogram | How are customer satisfaction ratings distributed across the fleet? |

---

## 3. Interactive Dashboards (3 Layouts)

1. **Market Overview:**
   - **Components:** Executive KPI Cards (Total Models, Total Sales, Avg Price, Avg Range), Sales by Category, Sales by Year, Top N Manufacturers, Region vs Average Price.
   - **Interactivity:** Category and Region cross-filtering enabled.
2. **Technology:**
   - **Components:** Battery Share Donut, Battery Durability (Cycle Life vs 5-Yr Degradation), Price vs Range Scatter, Category x Drivetrain Heatmap.
   - **Interactivity:** Battery chemistry highlighter and category filters.
3. **Geography and Impact:**
   - **Components:** Manufacturing Country Filled Map, Recommended Use Case Treemap, CO₂ Saved Stacked Bar, Customer Rating Histogram.
   - **Interactivity:** Map click-to-filter regional distributions.

---

## 4. Tableau Story Structure (6 Scenes)

- **Scene 1: Market Snapshot** — Overview of 100,000 models, $65,010 avg price, 324 km avg range.
- **Scene 2: Who Sells the Most** — Two-wheeler scooters (85.0M), sedans (78.3M), compact SUVs (76.1M) driving bulk volume.
- **Scene 3: Price vs Range** — Battery capacity is the primary driver of vehicle price (r = 0.84), rather than range alone.
- **Scene 4: Battery Technology** — Solid-State (2,999 cycles, 7.4% degradation) and LFP (2,498 cycles, 10.1% degradation) offer superior durability over NMC/NCA.
- **Scene 5: Regions and Countries** — Balanced global market presence without single-region monopoly.
- **Scene 6: Strategic Recommendations** — Growth opportunities in high-volume urban commuters and durable battery architectures.

---

## 5. Calculated Fields and Parameters

- **`Range per $1000`**:
  ```tableau
  [range_km] / [price_usd] * 1000
  ```
- **`Price Segment`**:
  ```tableau
  IF [price_usd] < 20000 THEN "Budget"
  ELSEIF [price_usd] < 60000 THEN "Mid-range"
  ELSEIF [price_usd] < 120000 THEN "Premium"
  ELSE "Luxury" END
  ```
- **`Range Class`**:
  ```tableau
  IF [range_km] >= 450 THEN "Long"
  ELSEIF [range_km] >= 250 THEN "Medium"
  ELSE "Short" END
  ```
- **`Fast Charge Rating`**:
  ```tableau
  IF [charging_dc_fast_time_min] <= 15 THEN "Ultra-fast"
  ELSEIF [charging_dc_fast_time_min] <= 25 THEN "Fast"
  ELSE "Standard" END
  ```
- **`Revenue (Est.)`**:
  ```tableau
  [price_usd] * [annual_sales_units]
  ```
- **`Sales Share %`**:
  ```tableau
  SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))
  ```
- **Parameter `Top N Manufacturers`**: Integer range [5, 30], default = 10.
- **`Is Top N`**:
  ```tableau
  RANK(SUM([annual_sales_units])) <= [Top N Manufacturers]
  ```

---

## 6. How to Open and Publish
1. Open `EV Market Analysis.twbx` using **Tableau Desktop** or **Tableau Public Edition** (v2020.4 or newer).
2. The workbook is fully self-contained using an embedded Hyper extract.
3. To publish: Click **Server > Tableau Public > Save to Tableau Public As...**, log in, and save under your profile.
