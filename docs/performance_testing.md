# Performance Testing & Optimization Record

**Project:** EV Market Analysis  
**Student:** Nipun Jain  
**Environment:** Tableau Public 2024+ / Python 3.14 / SQLite & MySQL  

---

## 1. Workload Metrics

| Parameter | Measured Specification |
|---|---|
| **Underlying Records Rendered** | Exactly 100,000 records (`ev_market_test.csv`) |
| **Attribute Width** | 37 original columns + 5 derived calculated fields |
| **Global Data Filters** | 6 synchronized across all sheets (`model_year`, `market_region`, `category`, `battery_type`, `price_segment`, `Top N`) |
| **Calculated Fields** | 6 business metrics + 1 dynamic ranking filter |
| **Visualizations Built** | 12 dedicated worksheets |
| **Coordinated Dashboards** | 3 responsive dashboards |
| **Story Points** | 6 narrative scenes |
| **Web Integration** | Flask 3.1.3 embedding Tableau API v3 |

---

## 2. Benchmark Observations & Optimization Strategies

1. **Extract Architecture:**
   - Utilizing an extracted `.hyper` data file reduced query latency from several seconds over live database connections down to sub-second rendering (< 0.8s) during dashboard cross-filtering.
2. **Top N Parameter Optimization:**
   - Rather than plotting all 200 distinct manufacturers on a single chart (which causes high visual mark clutter and DOM overhead), the `Is Top N` calculated field restricts rendering to 10–20 marks dynamically.
3. **Scatter Plot Aggregation:**
   - The Price vs Range visualization applies category filtering to avoid excessive DOM element count while retaining individual model point exploration.
4. **Shared Filter Context:**
   - All 6 interactive filters are set to "All Using Related Data Sources" to avoid redundant individual data passes across worksheets.
