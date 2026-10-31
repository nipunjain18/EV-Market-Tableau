"""Production readiness test suite for EV360 Web Application.
Tests all 10 verification points requested for Render deployment.
"""
import os
import sys
import unittest
import urllib.request
from bs4 import BeautifulSoup

# Ensure app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, TABLEAU_DASHBOARD_URL, TABLEAU_STORY_URL, BASE_DIR


class TestEV360Deployment(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_homepage_loads(self):
        """1. Homepage loads successfully with HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("EV360", html)
        self.assertIn("Understand markets", html)
        self.assertIn("DATA-DRIVEN EV INTELLIGENCE", html)

    def test_02_all_flask_routes_work(self):
        """2. All Flask routes work correctly."""
        # Root
        resp_root = self.client.get("/")
        self.assertEqual(resp_root.status_code, 200)

        # Redirect routes
        for path, anchor in [("/dashboard", "#dashboard"), ("/story", "#story"), ("/about", "#about"), ("/faq", "#faq")]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 302, f"Route {path} should return 302 redirect")
            self.assertIn(anchor, resp.headers.get("Location", ""))

        # Health endpoint
        resp_health = self.client.get("/health")
        self.assertEqual(resp_health.status_code, 200)
        self.assertEqual(resp_health.get_json().get("status"), "healthy")

    def test_03_dashboard_section_works(self):
        """3. Dashboard section works and embedded viz is present."""
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find("section", id="dashboard")
        self.assertIsNotNone(section, "Dashboard section (#dashboard) must exist")
        viz = soup.find("tableau-viz", id="tableauDashboard")
        self.assertIsNotNone(viz, "Tableau Dashboard web component must exist")
        self.assertEqual(viz.get("src"), TABLEAU_DASHBOARD_URL)

    def test_04_tableau_story_loads(self):
        """4. Tableau Story section and script load."""
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find("section", id="story")
        self.assertIsNotNone(section, "Story section (#story) must exist")
        viz = soup.find("tableau-viz", id="tableauStory")
        self.assertIsNotNone(viz, "Tableau Story web component must exist")
        self.assertEqual(viz.get("src"), TABLEAU_STORY_URL)

        # Verify Tableau Embedding API v3 script tag is included
        script = soup.find("script", src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js")
        self.assertIsNotNone(script, "Tableau Embedding API v3 script tag must be present")

    def test_05_about_section_works(self):
        """5. About section exists with verified statistics."""
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find("section", id="about")
        self.assertIsNotNone(section, "About section (#about) must exist")
        self.assertIn("100,000 Verified Records", html)
        self.assertIn("Multi-Dimensional Analytics", html)
        self.assertIn("Interactive BI Integration", html)

    def test_06_faq_section_works(self):
        """6. FAQ section contains interactive accordion items."""
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find("section", id="faq")
        self.assertIsNotNone(section, "FAQ section (#faq) must exist")
        items = soup.find_all("div", class_="faq-item")
        self.assertGreaterEqual(len(items), 4, "Should have at least 4 FAQ items")

    def test_07_project_report_opens(self):
        """7. Project report route opens PDF inline."""
        response = self.client.get("/report")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        data = response.get_data()
        response.close()
        self.assertTrue(data.startswith(b"%PDF"), "Report should be a valid PDF file")
        expected_size = os.path.getsize(os.path.join(BASE_DIR, "docs", "EV_Market_Tableau_Project_Report.pdf"))
        self.assertEqual(len(data), expected_size)

    def test_08_pdf_download_works(self):
        """8. PDF download route provides file as attachment."""
        response = self.client.get("/download/report")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        disp = response.headers.get("Content-Disposition", "")
        self.assertIn("attachment", disp)
        self.assertIn("EV_Market_Tableau_Project_Report.pdf", disp)
        data = response.get_data()
        response.close()
        self.assertTrue(data.startswith(b"%PDF"))

    def test_09_dataset_download_works(self):
        """9. Dataset download route provides raw CSV as attachment."""
        response = self.client.get("/download/data")
        self.assertEqual(response.status_code, 200)
        disp = response.headers.get("Content-Disposition", "")
        self.assertIn("attachment", disp)
        self.assertIn("ev_market_test.csv", disp)
        data = response.get_data()
        response.close()
        expected_size = os.path.getsize(os.path.join(BASE_DIR, "data", "raw", "ev_market_test.csv"))
        self.assertEqual(len(data), expected_size)
        # Check first line is header with 37 columns
        first_line = data[:500].decode("utf-8").split("\n")[0]
        self.assertIn("model_year", first_line)
        self.assertIn("price_usd", first_line)

    def test_10_static_assets_load(self):
        """10. Static CSS asset loads correctly."""
        response = self.client.get("/static/css/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.mimetype)
        css_text = response.get_data(as_text=True)
        response.close()
        self.assertIn(".hero-grid", css_text)
        self.assertIn(".btn-terracotta", css_text)


if __name__ == "__main__":
    unittest.main()
