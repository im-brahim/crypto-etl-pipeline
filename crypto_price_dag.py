from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, json, os

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

        # Add timestamp
        data["timestamp"] = datetime.utcnow().isoformat()

        # Append to file
        file_path = "/opt/airflow/data/crypto.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        else:
            existing = []

        existing.append(data)

        with open(file_path, "w") as f:
            json.dump(existing, f, indent=2)

    except Exception as e:
        print(f"Error: {e}")

with DAG(
    dag_id="crypto_price_hourly",
    default_args=default_args,
    start_date=datetime(2025, 4, 15),
    schedule_interval='@hourly',  # or '0 * * * *'
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="fetch_crypto_data",
        python_callable=fetch_and_save
    )
