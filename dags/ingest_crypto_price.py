from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import requests, json
import boto3 # type: ignore

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

MINIO_ACCESS_KEY = "minio"
MINIO_ENDPOINT = "http://minio:9000"
MINIO_SECRET_KEY = "00000000"

def upload_to_minio(file_path, bucket_name, object_name):
    s3_client = boto3.client(
        's3',
        endpoint_url= MINIO_ENDPOINT,
        aws_access_key_id= MINIO_ACCESS_KEY,
        aws_secret_access_key= MINIO_SECRET_KEY,
        region_name='us-east-1',
    )
    s3_client.upload_file(file_path, bucket_name, object_name)


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
    dag_id="ingest_crypto_price",
    default_args=default_args,
    start_date=datetime(2025, 4, 15),
    schedule_interval='*/1 * * * *',         # every minute: '*/1 * * * *',       # every hour: '@hourly', 
    catchup=False,
    tags=["ingestion", "API_crypto", "MinIO"]
) as dag:

    task = PythonOperator(
        task_id="fetch_crypto_data",
        python_callable=fetch_and_save
    )
