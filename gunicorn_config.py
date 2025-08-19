"""
Gunicorn configuration file for deploying the Gaming AI Chatbot on Render.
"""

# Gunicorn configuration
bind = "0.0.0.0:$PORT"
workers = 2
threads = 2
timeout = 120
worker_class = "gthread"
accesslog = "-"
