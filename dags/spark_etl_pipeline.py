from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="spark_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 4, 17),
    schedule_interval='@hourly',  # Every hour
    catchup=False
) as dag:

# Task 1: read_from_minio:
read_from_minio = DockerOperator(
    task_id='read_from_minio',
    image='bitnami/spark:3.5.0',
    command='spark-submit /opt/spark/jobs/read_crypto_from_minio.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='etl-network',
    volumes=['./jobs:/opt/spark/jobs'],
    dag=dag
)

# Task 2: process_data
process_data = DockerOperator(
    task_id='process_data',
    image='bitnami/spark:3.5.0',
    command='spark-submit /opt/spark/jobs/process_crypto.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='etl-network',
    volumes=['./jobs:/opt/spark/jobs'],
    dag=dag
)

# Task 3: save_to_db
save_to_db = DockerOperator(
    task_id='save_to_db',
    image='bitnami/spark:3.5.0',
    command='spark-submit /opt/spark/jobs/save_to_db.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='etl-network',
    volumes=['./jobs:/opt/spark/jobs'],
    dag=dag
)

# Task dependencies:
read_from_minio >> process_data >> save_to_db