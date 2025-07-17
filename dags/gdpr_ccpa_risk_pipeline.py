"""
DAG: gdpr_ccpa_risk_pipeline

Description:
Automated pipeline to fetch real-time GDPR regulatory updates from the European Data Protection Board (EDPB),
process them for downstream analysis and forecasting, and output structured data for risk modeling.

Source:
https://edpb.europa.eu/news/news_en
"""

# dags/gdpr_ccpa_risk_pipeline.py

import os
import sys

# Ensure scripts/ is importable by adding the project root to PYTHONPATH
dag_folder = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(dag_folder, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import script functions
try:
    from scripts.fetch_policy_data import fetch_policy_data
    from scripts.process_policy_data import process_policy_data
    from scripts.forecast_policy_trends import forecast_policy_trends
except ImportError as e:
    raise ImportError(f"Error importing scripts modules: {e}")

# Default task arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="gdpr_ccpa_risk_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
    tags=["gdpr", "ccpa", "risk_pipeline"],
) as dag:

    # Download raw EDPB news
    fetch = PythonOperator(
        task_id="fetch_policy_data",
        python_callable=fetch_policy_data,
    )

    # Process raw JSON into structured CSV
    process = PythonOperator(
        task_id="process_policy_data",
        python_callable=process_policy_data,
    )

    # Forecast trends
    forecast = PythonOperator(
        task_id="forecast_policy_trends",
        python_callable=lambda: forecast_policy_trends(periods=7),
    )

    fetch >> process >> forecast

    
