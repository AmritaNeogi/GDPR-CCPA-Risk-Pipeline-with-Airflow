from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Step 1: Add the project root to sys.path
# Assumes this file is in `dags/` and `scripts/` is in the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Step 2: Now we can safely import the script
from scripts.fetch_policy_data import fetch_policy_data
from scripts.process_policy_data import process_policy_data
from scripts.forecast_policy_trends import forecast_policy_trends

# Step 3: DAG definition
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='gdpr_ccpa_risk_pipeline',
    default_args=default_args,
    description='Fetch, process & forecast GDPR/CCPA policy updates hourly',
    schedule_interval='@hourly',
    start_date=datetime(2025, 7, 15),
    catchup=False,
    tags=['gdpr', 'ccpa', 'risk'],
) as dag:

    task_fetch = PythonOperator(
        task_id='fetch_policy_data',
        python_callable=fetch_policy_data,
    )

    task_process = PythonOperator(
        task_id='process_policy_data',
        python_callable=process_policy_data,
    )

    task_forecast = PythonOperator(
        task_id='forecast_policy_trends',
        python_callable=forecast_policy_trends,
    )

    task_fetch >> task_process >> task_forecast
