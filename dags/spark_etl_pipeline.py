from airflow import DAG # type: ignore
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator # type: ignore


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="spark_etl_from_minio_to_db",
    default_args=default_args,
    description="ETL pipeline to process data from MinIO and load into PostgreSQL",
    start_date=datetime(2025, 4, 17),
    schedule_interval="@hourly",
    catchup=False,
    tags=["Spark", "ETL", "MinIO", "DB"]
) as dag:

    #/opt/bitnami/spark/bin/
    # # Task 1: Read JSON from MinIO & Process It
    process_data = BashOperator(
        task_id='read_process_json',
        bash_command="""
            docker exec master spark-submit \
            --master spark://master:7077 \
            /opt/spark/jobs/process_data.py
        """
    )

    # Task 2: Compare Data
    compare_data = BashOperator(
        task_id='compare_data',
        bash_command="""
            docker exec master spark-submit \
            --master spark://master:7077 \
            --jars /opt/spark/jars/postgresql-42.6.0.jar \
            /opt/spark/jobs/compare_data.py
        """
    )

    # Task 3: Save to PostgreSQL
    save_to_db = BashOperator(
        task_id='save_to_db',
        bash_command="""
            docker exec master /opt/bitnami/spark/bin/spark-submit \
            --master spark://master:7077 \
            --jars /opt/spark/jars/postgresql-42.6.0.jar \
            /opt/spark/jobs/save_to_db.py
        """    
    )

    # Set task dependencies
    process_data >> compare_data >> save_to_db
