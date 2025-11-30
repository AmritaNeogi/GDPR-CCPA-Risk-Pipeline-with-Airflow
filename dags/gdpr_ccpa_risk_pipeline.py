"""
DAG: gdpr_ccpa_risk_pipeline

Description:
Automated pipeline to fetch real-time GDPR regulatory updates from the
European Data Protection Board (EDPB), process them for downstream analysis
and forecasting, validate the outputs, and write structured data for
regulatory risk modeling.

Source:
https://edpb.europa.eu/news/news_en
"""

import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# ---------------------------------------------------------------------
# Ensure the project root is on PYTHONPATH so we can import gdpr_pipeline
# ---------------------------------------------------------------------
dag_folder = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(dag_folder, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import from the package API (gdpr_pipeline/__init__.py)
from gdpr_pipeline import (
    fetch_policy_data,
    process_policy_data,
    validate_latest_xml,
    forecast_policy_trends,
)

# ---------------------------------------------------------------------
# Default task arguments
# ---------------------------------------------------------------------
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# ---------------------------------------------------------------------
# DAG definition
# ---------------------------------------------------------------------
with DAG(
    dag_id="gdpr_ccpa_risk_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
    tags=["gdpr", "ccpa", "risk_pipeline"],
) as dag:

    # 1) Download raw EDPB news (JSON files under data/raw)
    fetch = PythonOperator(
        task_id="fetch_policy_data",
        python_callable=fetch_policy_data,
    )

    # 2) Process raw JSON into a cleaned CSV under data/processed
    process = PythonOperator(
        task_id="process_policy_data",
        python_callable=process_policy_data,
    )

    # 3) Run validation checks on the latest XML/processed file
    validate = PythonOperator(
        task_id="validate_policy_data",
        python_callable=validate_latest_xml,
    )

    # 4) Forecast policy trends (volume / severity by time)
    forecast = PythonOperator(
        task_id="forecast_policy_trends",
        python_callable=lambda: forecast_policy_trends(periods=7),
    )

    # Task dependencies: fetch → process → validate → forecast
    fetch >> process >> validate >> forecast
