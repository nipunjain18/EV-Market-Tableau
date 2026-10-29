"""Flask Web Application for EV Market Analysis.
Embeds Tableau Public interactive dashboards and stories.
Author: Nipun Jain
"""
import os
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)

# Defaults configured for Nipun Jain's published Tableau Public project
DEFAULT_STORY_URL = "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
DEFAULT_DASHBOARD_URL = "https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview"

DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", DEFAULT_DASHBOARD_URL)
STORY_URL = os.getenv("TABLEAU_STORY_URL", DEFAULT_STORY_URL)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", viz_url=DASHBOARD_URL)


@app.route("/story")
def story():
    return render_template("story.html", viz_url=STORY_URL)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"Starting EV Market Analytics Web App on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
