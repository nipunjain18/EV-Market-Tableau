"""Gunicorn production configuration for Render deployment.
EV Market Analysis (EV360) Web Portal
Author: Nipun Jain
"""
import os

# Dynamic port binding: Render automatically assigns the PORT environment variable
port = os.getenv("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Concurrency settings: optimized for memory efficiency on Render free tier (512MB RAM)
workers = int(os.getenv("WEB_CONCURRENCY", "2"))
threads = int(os.getenv("PYTHON_GET_THREADS", "2"))
worker_class = "gthread"

# Timeout settings to handle initial container spin-up and larger PDF/data downloads
timeout = 120
keepalive = 5

# Direct stdout/stderr logging for Render Live Logs
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")

