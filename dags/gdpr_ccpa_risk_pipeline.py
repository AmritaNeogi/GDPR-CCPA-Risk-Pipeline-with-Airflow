# dags/gdpr_ccpa_risk_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 7, 16),
}

def fetch_policy():
    from scripts.fetch_policy_data import fetch_policy_data
    fetch_policy_data()

def process_policy():
    from scripts.process_policy_data import process_policy_data
    process_policy_data()

def forecast_policy():
    from scripts.forecast_policy_trends import forecast_policy_trends
    # forecast next 7 days
    forecast_policy_trends(periods=7)

with DAG(
    dag_id="gdpr_ccpa_risk_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
    description="Fetch, process & forecast GDPR/CCPA policy updates hourly",
) as dag:

    task_fetch = PythonOperator(
        task_id="fetch_policy_data",
        python_callable=fetch_policy,
    )

    task_process = PythonOperator(
        task_id="process_policy_data",
        python_callable=process_policy,
    )

    task_forecast = PythonOperator(
        task_id="forecast_policy_trends",
        python_callable=forecast_policy,
    )

    # Chain all three
    task_fetch >> task_process >> task_forecast
