# Databricks notebook source
# COMMAND ----------
# Install Streamlit if not already installed
# %pip install streamlit

# COMMAND ----------
import subprocess
import sys
import os

# Set working directory to the repo
os.chdir("/Workspace/Repos/YOUR_USER/databricks-app")

# Run the Streamlit app
subprocess.run([
    sys.executable, 
    "-m", 
    "streamlit", 
    "run", 
    "app.py",
    "--client.showErrorDetails=false",
    "--logger.level=warning",
    "--server.port=8501",
    "--server.headless=true"
])
