"""Electric Vehicle Market Analytics (EV360) Web Application.
Author: Nipun Jain
"""
import os
import time
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, send_from_directory

load_dotenv()
app = Flask(__name__)

TABLEAU_STORY_URL = os.getenv(
    "TABLEAU_STORY_URL",
    "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
)
TABLEAU_DASHBOARD_URL = os.getenv(
    "TABLEAU_DASHBOARD_URL",
    "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview"
)
GITHUB_URL = "https://github.com/nipunjain18/EV-Market-Tableau"
DEMO_VIDEO_URL = "https://drive.google.com/file/d/1bhgJYTCFo_HUNPkSzLFqEuRo9CGH60u0/view?usp=drive_link"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.context_processor
def inject_global_data():
    return {
        "student_name": "Nipun Jain",
        "github_url": GITHUB_URL,
        "demo_video_url": DEMO_VIDEO_URL,
        "tableau_dashboard_url": TABLEAU_DASHBOARD_URL,
        "tableau_story_url": TABLEAU_STORY_URL,
        "current_year": time.strftime("%Y")
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        dashboard_url=TABLEAU_DASHBOARD_URL,
        story_url=TABLEAU_STORY_URL
    )


@app.route("/dashboard")
def dashboard():
    return redirect(f"{url_for('home')}#dashboard")


@app.route("/story")
def story():
    return redirect(f"{url_for('home')}#story")


@app.route("/about")
def about():
    return redirect(f"{url_for('home')}#about")


@app.route("/faq")
def faq():
    return redirect(f"{url_for('home')}#faq")


@app.route("/report")
def report():
    return send_from_directory(
        os.path.join(BASE_DIR, "docs"),
        "EV_Market_Tableau_Project_Report.pdf"
    )


@app.route("/download/report")
def download_report():
    return send_from_directory(
        os.path.join(BASE_DIR, "docs"),
        "EV_Market_Tableau_Project_Report.pdf",
        as_attachment=True
    )


@app.route("/download/data")
def download_data():
    raw_path = os.path.join(BASE_DIR, "data", "raw")
    return send_from_directory(raw_path, "ev_market_test.csv", as_attachment=True)


@app.route("/health")
def health():
    return {"status": "healthy", "service": "EV360 Analytics"}, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    print(f"Starting EV360 Web App on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
