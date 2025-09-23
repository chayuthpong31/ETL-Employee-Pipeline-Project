import datetime
from airflow import DAG
try:
  from airflow.providers.standard.operators.bash import BashOperator
except ImportError:
  from airflow.operators.bash_operator import BaashOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args = {
    'start_date': datetime.datetime(2025, 9, 22),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG(
    'employee_data',
    default_args=default_args,
    description='Run python scripts',
    schedule='@daily',
    catchup=False,
)

with dag:
    run_script_task = BashOperator(
    task_id = 'extract_data',
    bash_command = 'python3 /home/airflow/gcs/dags/scripts/load_into_gcs.py'
  ),

    start_pipeline = CloudDataFusionStartPipelineOperator(
    location='us-central1',
    pipeline_name='etl-pipeline',
    instance_name='datafusion-dev',
    task_id="start_datfusion_pipeline",
    pipeline_timeout=1000,
)
    
run_script_task >> start_pipeline