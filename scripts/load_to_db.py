"""Database loader script for EV Market Analysis.
Loads the 100,000-record ev_market_test.csv into SQLite (default) or MySQL.
Author: Nipun Jain
"""
import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "ev_market_test.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Dataset not found at {raw_path}")

    print(f"Reading dataset from {raw_path}...")
    df = pd.read_csv(raw_path)
    print(f"Dataset loaded into memory: {len(df):,} rows, {len(df.columns)} columns.")

    use_mysql = os.getenv("USE_MYSQL", "false").lower() in ("true", "1", "yes")

    if use_mysql:
        try:
            from sqlalchemy import create_engine
            db_user = os.getenv("DB_USER", "root")
            db_pass = os.getenv("DB_PASSWORD", "")
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "3306")
            db_name = os.getenv("DB_NAME", "ev_db")
            url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            engine = create_engine(url)
            print(f"Connecting to MySQL ({db_host}:{db_port}/{db_name})...")
            df.to_sql("ev_market", engine, if_exists="replace", index=False, chunksize=5000)
            print(f"Successfully loaded {len(df):,} rows into MySQL table 'ev_market'.")
        except Exception as e:
            print(f"MySQL loading failed: {e}")
            print("Falling back to SQLite database...")
            load_to_sqlite(df, base_dir)
    else:
        load_to_sqlite(df, base_dir)

def load_to_sqlite(df, base_dir):
    db_path = os.path.join(base_dir, "data", "ev_market.db")
    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql("ev_market", conn, if_exists="replace", index=False)
    
    # Create indexes for analytical speed
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_category ON ev_market(category);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_year ON ev_market(model_year);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_region ON ev_market(market_region);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer ON ev_market(manufacturer);")
    conn.commit()

    # Create analytical view vw_ev_clean
    cur.execute("""
    CREATE VIEW IF NOT EXISTS vw_ev_clean AS
    SELECT *,
           ROUND(range_km / price_usd * 1000, 2) AS range_per_1000usd,
           CASE WHEN price_usd < 20000 THEN 'Budget'
                WHEN price_usd < 60000 THEN 'Mid-range'
                WHEN price_usd < 120000 THEN 'Premium' ELSE 'Luxury' END AS price_segment,
           CASE WHEN range_km < 250 THEN 'Short'
                WHEN range_km < 450 THEN 'Medium' ELSE 'Long' END AS range_class,
           ROUND(price_usd * annual_sales_units, 2) AS est_revenue_usd
    FROM ev_market
    WHERE price_usd > 0 AND range_km > 0;
    """)
    conn.commit()

    count = cur.execute("SELECT COUNT(*) FROM ev_market").fetchone()[0]
    conn.close()
    print(f"Successfully loaded {count:,} rows into SQLite database 'ev_market.db' with view 'vw_ev_clean'.")

if __name__ == "__main__":
    load_data()
