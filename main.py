#!/usr/bin/env python3
"""
Entry point for Databricks Apps deployment.
Ensures streamlit runs with the correct context.
"""
import subprocess
import sys

if __name__ == "__main__":
    # Run streamlit with proper arguments for Databricks
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--client.showErrorDetails=false",
        "--logger.level=warning",
    ]
    sys.exit(subprocess.call(cmd))
