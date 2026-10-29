-- =====================================================================
-- Project: EV Market Analysis
-- Student: Nipun Jain
-- SQL Analytical Queries (Tested against 100,000-record reference dataset)
-- =====================================================================

-- 0. Dataset Sanity Checks
SELECT COUNT(*) AS total_records FROM ev_market;
-- Expected: 100,000 rows

SELECT 
    COUNT(DISTINCT manufacturer) AS unique_manufacturers,
    COUNT(DISTINCT category) AS unique_categories,
    COUNT(DISTINCT manufacturing_country) AS unique_countries,
    COUNT(DISTINCT market_region) AS unique_regions,
    COUNT(DISTINCT battery_type) AS unique_battery_types,
    COUNT(DISTINCT recommended_use_case) AS unique_use_cases
FROM ev_market;

-- 1. Top 10 Manufacturers by Total Annual Sales Units
SELECT 
    manufacturer, 
    CAST(SUM(annual_sales_units) AS BIGINT) AS total_annual_sales,
    ROUND(AVG(price_usd), 2) AS avg_vehicle_price,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_market 
WHERE annual_sales_units IS NOT NULL
GROUP BY manufacturer 
ORDER BY total_annual_sales DESC 
LIMIT 10;

-- 2. Sales Volume and Average Pricing by Category
SELECT 
    category, 
    COUNT(*) AS total_models, 
    CAST(SUM(annual_sales_units) AS BIGINT) AS total_sales_units,
    ROUND(AVG(price_usd), 2) AS avg_price_usd,
    ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_market 
GROUP BY category 
ORDER BY total_sales_units DESC;

-- 3. Battery Technology Performance & Durability Comparison
SELECT 
    battery_type,
    COUNT(*) AS model_count,
    ROUND(AVG(range_km), 1) AS avg_range_km,
    ROUND(AVG(charging_dc_fast_time_min), 1) AS avg_fast_charge_min,
    ROUND(AVG(battery_cycle_life), 0) AS avg_cycle_life,
    ROUND(AVG(battery_degradation_pct_5yr), 2) AS avg_5yr_degradation_pct
FROM ev_market 
GROUP BY battery_type 
ORDER BY avg_cycle_life DESC;

-- 4. Regional Market Breakdown & Environmental Impact
SELECT 
    market_region, 
    COUNT(*) AS model_count, 
    ROUND(AVG(price_usd), 2) AS avg_price_usd,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    ROUND(SUM(co2_saved_tons_per_year), 1) AS total_co2_saved_tons
FROM ev_market 
GROUP BY market_region 
ORDER BY model_count DESC;

-- 5. Model Year Evolution Trends (2018 - 2026)
SELECT 
    model_year, 
    COUNT(*) AS models_released, 
    ROUND(AVG(range_km), 1) AS avg_range_km,
    ROUND(AVG(price_usd), 2) AS avg_price_usd,
    CAST(SUM(annual_sales_units) AS BIGINT) AS total_sales_units
FROM ev_market 
GROUP BY model_year 
ORDER BY model_year ASC;

-- 6. Top 20 Best Value Vehicles (Range per $1,000 USD)
SELECT 
    model_name, 
    manufacturer, 
    category, 
    price_usd, 
    range_km,
    ROUND(range_km / price_usd * 1000, 2) AS km_per_1000usd
FROM ev_market 
WHERE price_usd > 0
ORDER BY km_per_1000usd DESC 
LIMIT 20;

-- 7. Manufacturing Country Analysis (Production & Safety Ratings)
SELECT 
    manufacturing_country, 
    COUNT(*) AS models_produced, 
    ROUND(AVG(safety_rating_stars), 2) AS avg_safety_rating,
    ROUND(AVG(price_usd), 2) AS avg_price_usd
FROM ev_market 
GROUP BY manufacturing_country 
ORDER BY models_produced DESC;

-- 8. Recommended Use-Case Distribution & Commercial Characteristics
SELECT 
    recommended_use_case, 
    COUNT(*) AS model_count, 
    ROUND(AVG(price_usd), 2) AS avg_price_usd,
    ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_market 
GROUP BY recommended_use_case 
ORDER BY model_count DESC;

-- 9. Comprehensive Data Quality and Null Audit
SELECT 
    SUM(resale_value_pct_3yr IS NULL) AS null_resale_count,
    SUM(battery_cycle_life IS NULL) AS null_cycle_life_count,
    SUM(customer_rating IS NULL) AS null_rating_count,
    SUM(infotainment_screen_inch IS NULL) AS null_screen_count,
    SUM(annual_sales_units IS NULL) AS null_sales_count,
    COUNT(*) AS total_rows
FROM ev_market;

-- 10. Drivetrain Architecture Across Categories
SELECT 
    category,
    drivetrain,
    COUNT(*) AS model_count,
    ROUND(AVG(price_usd), 2) AS avg_price_usd
FROM ev_market
GROUP BY category, drivetrain
ORDER BY category, model_count DESC;
