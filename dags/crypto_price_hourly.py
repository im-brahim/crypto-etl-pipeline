from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, json, os
import boto3

def upload_to_minio(file_path, bucket_name, object_name):
    s3_client = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='00000000',
        region_name='us-east-1',
    )
    s3_client.upload_file(file_path, bucket_name, object_name)

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_save():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        res = requests.get(url)
        data = res.json()

        # Handle API rate limit error
        if "error" in data or "status" in data:
            print("API Rate Limit Exceeded or Error:", data)
            return

        # Add timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Append as a new line (JSONL style)
        file_path = "/opt/airflow/data/crypto.json"
        with open(file_path, "a") as f:
            f.write(json.dumps(data) + "\n")

        # Upload to MinIO
        upload_to_minio(file_path, "crypto", "crypto.json")

    except Exception as e:
        print(f"Error: {e}")

with DAG(
    dag_id="crypto_price_hourly",
    default_args=default_args,
    start_date=datetime(2025, 4, 15),
    schedule_interval='@hourly',         # every minute: '*/1 * * * *',       # every hour: '@hourly', 
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="fetch_crypto_data",
        python_callable=fetch_and_save
    )
