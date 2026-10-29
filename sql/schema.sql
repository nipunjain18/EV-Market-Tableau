-- =====================================================================
-- Project: EV Market Analysis
-- Student: Nipun Jain
-- Database Schema Definition (Compatible with MySQL and SQLite)
-- =====================================================================

-- For MySQL: Create database and switch context
CREATE DATABASE IF NOT EXISTS ev_db;
USE ev_db;

-- Table definition for ev_market (100,000 rows, 37 columns)
CREATE TABLE IF NOT EXISTS ev_market (
    vehicle_id VARCHAR(50) PRIMARY KEY,
    model_name VARCHAR(100),
    manufacturer VARCHAR(100),
    model_year INT,
    manufacturing_country VARCHAR(100),
    market_region VARCHAR(100),
    category VARCHAR(100),
    battery_capacity_kwh FLOAT,
    battery_type VARCHAR(50),
    battery_cycle_life FLOAT,
    battery_degradation_pct_5yr FLOAT,
    range_km FLOAT,
    efficiency_wh_per_km FLOAT,
    motor_power_kw FLOAT,
    torque_nm FLOAT,
    num_motors INT,
    drivetrain VARCHAR(20),
    top_speed_kmph FLOAT,
    acceleration_0_100_sec FLOAT,
    max_dc_charging_kw FLOAT,
    charging_dc_fast_time_min FLOAT,
    charging_ac_time_hr FLOAT,
    num_charging_ports INT,
    num_seats INT,
    weight_kg FLOAT,
    cargo_capacity_liters FLOAT,
    price_usd FLOAT,
    insurance_cost_usd_yearly FLOAT,
    warranty_years INT,
    resale_value_pct_3yr FLOAT,
    safety_rating_stars FLOAT,
    autonomous_level INT,
    infotainment_screen_inch FLOAT,
    co2_saved_tons_per_year FLOAT,
    annual_sales_units FLOAT,
    customer_rating FLOAT,
    recommended_use_case VARCHAR(100)
);

-- Performance optimization indexes
CREATE INDEX IF NOT EXISTS idx_category ON ev_market(category);
CREATE INDEX IF NOT EXISTS idx_year ON ev_market(model_year);
CREATE INDEX IF NOT EXISTS idx_region ON ev_market(market_region);
CREATE INDEX IF NOT EXISTS idx_manufacturer ON ev_market(manufacturer);
CREATE INDEX IF NOT EXISTS idx_battery ON ev_market(battery_type);

-- Analytical View with Derived Fields matching Tableau Calculated Fields
CREATE OR REPLACE VIEW vw_ev_clean AS
SELECT *,
       ROUND(range_km / price_usd * 1000, 2) AS range_per_1000usd,
       CASE WHEN price_usd < 20000 THEN 'Budget'
            WHEN price_usd < 60000 THEN 'Mid-range'
            WHEN price_usd < 120000 THEN 'Premium' ELSE 'Luxury' END AS price_segment,
       CASE WHEN range_km < 250 THEN 'Short'
            WHEN range_km < 450 THEN 'Medium' ELSE 'Long' END AS range_class,
       CASE WHEN charging_dc_fast_time_min <= 15 THEN 'Ultra-fast'
            WHEN charging_dc_fast_time_min <= 25 THEN 'Fast' ELSE 'Standard' END AS fast_charge_rating,
       ROUND(price_usd * annual_sales_units, 2) AS est_revenue_usd
FROM ev_market
WHERE price_usd > 0 AND range_km > 0;
