import requests
from datetime import datetime, timezone 
from jobs.data_io import save_json_to_minio
from jobs.connect import create_spark_session, get_logger
from jobs.config import EXCHANGE_API_URL , EXCHANGE_RATE_PATH

logger = get_logger("Fetch Exchange Rate")
spark = create_spark_session("FetchExchangeRate")

# API and storage config
OBJECT_NAME = "usd_mad_rate.json"

def fetch_usd_mad():
    try:
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()
        data = response.json()

        usd_to_mad = data["rates"]["MAD"]
        timestamp = data["time_last_update_unix"] 
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        # date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        return [{
            "base": "USD",
            "target": "MAD",
            "rate": usd_to_mad,
            "date": date
        }]
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return []

def save_to_minio(data):
    
    if data:
        df = spark.createDataFrame(data)
        save_json_to_minio(df,f"{EXCHANGE_RATE_PATH}usd_mad_rate.json")

        logger.info(f"✅ Exchange rate saved to {EXCHANGE_RATE_PATH}usd_mad_rate.json")
    else:
        logger.warning("⚠️ No data to save")

   

if __name__ == "__main__":

    data = fetch_usd_mad()
    save_to_minio(data)

    spark.stop()
