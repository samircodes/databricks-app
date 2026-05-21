#!/usr/bin/env python3
"""
Databricks Apps entry script.
When Databricks launches the app with `python app.py`, this wrapper starts Streamlit properly.
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.headless=true",
        "--client.showErrorDetails=false",
        "--logger.level=warning",
    ]
    sys.exit(subprocess.call(cmd))
