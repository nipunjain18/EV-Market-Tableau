"""Data preparation script for EV Market Analysis.
Derives fields matching Tableau calculated fields from the 100,000-record ev_market_test.csv dataset.
Author: Nipun Jain
"""
import os
import pandas as pd

def clean_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "ev_market_test.csv")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    out_path = os.path.join(cleaned_dir, "ev_market_clean.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")

    print(f"Loading raw dataset from {raw_path}...")
    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df):,} records with {len(df.columns)} columns.")

    c = df.copy()

    # Derived field 1: Range per 1000 USD
    c["range_per_1000usd"] = (c["range_km"] / c["price_usd"] * 1000).round(2)

    # Derived field 2: Price Segment
    # Budget: < $20,000 | Mid-range: $20,000 - $59,999 | Premium: $60,000 - $119,999 | Luxury: >= $120,000
    c["price_segment"] = pd.cut(
        c["price_usd"],
        bins=[0, 20000, 60000, 120000, float("inf")],
        labels=["Budget", "Mid-range", "Premium", "Luxury"],
        right=False
    )

    # Derived field 3: Range Class
    # Short: < 250 km | Medium: 250 - 449 km | Long: >= 450 km
    c["range_class"] = pd.cut(
        c["range_km"],
        bins=[0, 250, 450, float("inf")],
        labels=["Short", "Medium", "Long"],
        right=False
    )

    # Derived field 4: Fast Charge Rating
    # Ultra-fast: <= 15 min | Fast: 16 - 25 min | Standard: > 25 min
    c["fast_charge_rating"] = pd.cut(
        c["charging_dc_fast_time_min"],
        bins=[0, 15.0001, 25.0001, float("inf")],
        labels=["Ultra-fast", "Fast", "Standard"],
        right=True
    )

    # Derived field 5: Estimated Revenue (USD)
    c["est_revenue_usd"] = (c["price_usd"] * c["annual_sales_units"]).round(2)

    os.makedirs(cleaned_dir, exist_ok=True)
    c.to_csv(out_path, index=False)
    print(f"Successfully processed and saved {len(c):,} rows to {out_path}")

if __name__ == "__main__":
    clean_data()
