"""Flask Web Application for EV Market Analysis.
Comprehensive Executive Business Intelligence Portal.
Author: Nipun Jain
"""
import os
import sqlite3
import time
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, send_from_directory, request

load_dotenv()
app = Flask(__name__)

# Defaults configured for Nipun Jain's published Tableau Public project
DEFAULT_STORY_URL = "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
DEFAULT_DASHBOARD_URL = "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview"

DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", DEFAULT_DASHBOARD_URL)
STORY_URL = os.getenv("TABLEAU_STORY_URL", DEFAULT_STORY_URL)
GITHUB_URL = "https://github.com/nipunjain18/EV-Market-Tableau"
DEMO_VIDEO_URL = "https://drive.google.com/file/d/1Oik0Z53AKzTwvmX7_oB2swu_yIT3qbFW/view?usp=drivesdk"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "ev_market.db")

QUERIES_CATALOG = {
    "top_manufacturers": {
        "title": "Top 10 Manufacturers by Sales Volume",
        "description": "Aggregates total annual sales units, average vehicle price, and customer ratings for leading brands.",
        "sql": """SELECT manufacturer, 
       CAST(SUM(annual_sales_units) AS BIGINT) AS total_annual_sales,
       ROUND(AVG(price_usd), 2) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_market 
WHERE annual_sales_units IS NOT NULL
GROUP BY manufacturer 
ORDER BY total_annual_sales DESC 
LIMIT 10;"""
    },
    "category_sales": {
        "title": "Sales Volume & Pricing by Category",
        "description": "Compares fleet size, cumulative sales volume, average price, and average range across 15 categories.",
        "sql": """SELECT category, 
       COUNT(*) AS total_models, 
       CAST(SUM(annual_sales_units) AS BIGINT) AS total_sales_units,
       ROUND(AVG(price_usd), 2) AS avg_price_usd,
       ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_market 
GROUP BY category 
ORDER BY total_sales_units DESC;"""
    },
    "battery_tech": {
        "title": "Battery Chemistry Benchmarks",
        "description": "Evaluates driving range, DC fast charging time, lifecycle cycles, and 5-year degradation rate across 5 chemistries.",
        "sql": """SELECT battery_type,
       COUNT(*) AS model_count,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(charging_dc_fast_time_min), 1) AS avg_fast_charge_min,
       ROUND(AVG(battery_cycle_life), 0) AS avg_cycle_life,
       ROUND(AVG(battery_degradation_pct_5yr), 2) AS avg_5yr_degradation_pct
FROM ev_market 
GROUP BY battery_type 
ORDER BY avg_cycle_life DESC;"""
    },
    "regional_performance": {
        "title": "Regional Market Breakdown & Impact",
        "description": "Summarizes model availability, average retail price, customer satisfaction, and total carbon displacement.",
        "sql": """SELECT market_region, 
       COUNT(*) AS model_count, 
       ROUND(AVG(price_usd), 2) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_rating,
       ROUND(SUM(co2_saved_tons_per_year), 1) AS total_co2_saved_tons
FROM ev_market 
GROUP BY market_region 
ORDER BY model_count DESC;"""
    },
    "yearly_trends": {
        "title": "Multi-Year Fleet Progression (2018–2026)",
        "description": "Annual model releases, average range progression, pricing trends, and annual sales volume.",
        "sql": """SELECT model_year, 
       COUNT(*) AS models_released, 
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(price_usd), 2) AS avg_price_usd,
       CAST(SUM(annual_sales_units) AS BIGINT) AS total_sales_units
FROM ev_market 
GROUP BY model_year 
ORDER BY model_year ASC;"""
    },
    "best_value": {
        "title": "Top 15 Best Value Vehicles (Range per $1,000)",
        "description": "Identifies the highest driving range return per dollar of vehicle acquisition cost.",
        "sql": """SELECT model_name, manufacturer, category, price_usd, range_km,
       ROUND(range_km / price_usd * 1000, 2) AS km_per_1000usd
FROM ev_market 
WHERE price_usd > 0
ORDER BY km_per_1000usd DESC 
LIMIT 15;"""
    },
    "manufacturing_countries": {
        "title": "Manufacturing Country Production & Safety",
        "description": "Assesses vehicle production footprint, average safety star rating, and price by manufacturing nation.",
        "sql": """SELECT manufacturing_country, 
       COUNT(*) AS models_produced, 
       ROUND(AVG(safety_rating_stars), 2) AS avg_safety_stars,
       ROUND(AVG(price_usd), 2) AS avg_price_usd
FROM ev_market 
GROUP BY manufacturing_country 
ORDER BY models_produced DESC;"""
    },
    "use_cases": {
        "title": "Operational Use-Case Segmentation",
        "description": "Analyzes market distribution and economic positioning across 7 primary operational profiles.",
        "sql": """SELECT recommended_use_case, 
       COUNT(*) AS model_count, 
       ROUND(AVG(price_usd), 2) AS avg_price_usd,
       ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_market 
GROUP BY recommended_use_case 
ORDER BY model_count DESC;"""
    }
}


def get_db_connection():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    return None


@app.context_processor
def inject_global_data():
    return {
        "student_name": "Nipun Jain",
        "github_url": GITHUB_URL,
        "demo_video_url": DEMO_VIDEO_URL,
        "tableau_dashboard_url": DASHBOARD_URL,
        "tableau_story_url": STORY_URL,
        "record_count": "100,000",
        "attribute_count": "37",
        "current_year": time.strftime("%Y")
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", viz_url=DASHBOARD_URL)


@app.route("/story")
def story():
    return render_template("story.html", viz_url=STORY_URL)


@app.route("/sql")
def sql_lab():
    default_key = request.args.get("query", "top_manufacturers")
    if default_key not in QUERIES_CATALOG:
        default_key = "top_manufacturers"
    
    query_info = QUERIES_CATALOG[default_key]
    results = []
    columns = []
    exec_time_ms = 0
    
    conn = get_db_connection()
    if conn:
        try:
            t0 = time.time()
            cursor = conn.execute(query_info["sql"])
            rows = cursor.fetchall()
            exec_time_ms = round((time.time() - t0) * 1000, 1)
            if rows:
                columns = list(rows[0].keys())
                results = [dict(row) for row in rows]
            conn.close()
        except Exception as e:
            print(f"Error running query {default_key}: {e}")
            if conn:
                conn.close()

    return render_template(
        "sql.html",
        queries=QUERIES_CATALOG,
        selected_key=default_key,
        selected_query=query_info,
        columns=columns,
        results=results,
        exec_time_ms=exec_time_ms
    )


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/query/<query_key>")
def api_query(query_key):
    if query_key not in QUERIES_CATALOG:
        return jsonify({"error": "Query not found"}), 404

    query_info = QUERIES_CATALOG[query_key]
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database file not accessible"}), 500

    try:
        t0 = time.time()
        cursor = conn.execute(query_info["sql"])
        rows = cursor.fetchall()
        exec_time_ms = round((time.time() - t0) * 1000, 1)
        columns = list(rows[0].keys()) if rows else []
        results = [dict(row) for row in rows]
        conn.close()
        return jsonify({
            "key": query_key,
            "title": query_info["title"],
            "sql": query_info["sql"],
            "columns": columns,
            "results": results,
            "row_count": len(results),
            "exec_time_ms": exec_time_ms
        })
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500


@app.route("/download/report")
def download_report():
    pdf_path = os.path.join(BASE_DIR, "EV_Market_Tableau_Project_Report.pdf")
    if os.path.exists(pdf_path):
        return send_from_directory(BASE_DIR, "EV_Market_Tableau_Project_Report.pdf", as_attachment=True)
    return "Report PDF file not found", 404


@app.route("/download/data")
def download_data():
    raw_path = os.path.join(BASE_DIR, "data", "raw")
    if os.path.exists(os.path.join(raw_path, "ev_market_test.csv")):
        return send_from_directory(raw_path, "ev_market_test.csv", as_attachment=True)
    return "Dataset file not found", 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"Starting EV Market Analytics Web App on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
