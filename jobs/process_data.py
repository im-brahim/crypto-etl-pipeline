import requests

from utils.connect import create_spark_session, get_logger
from utils.data_io import read_json_from_minio, save_parquet_to_minio, save_in_db
from pyspark.sql.functions import col, to_date, when
from scripts.rate import get_rate
from pyspark.errors import AnalysisException
from dotenv import load_dotenv #type:ignore
import os

load_dotenv()

def save_to_minio_parquet(df, logger) -> None:
    """
    Save the enriched DataFrame as Parquet to MinIO.
    
    Args:
        spark_df: The enriched Spark DataFrame to persist.
        logger: Logger instance for status messages.
    """    
    try:
        parquet_path = os.getenv("MINIO_PARQUET_PATH")
        save_parquet_to_minio(df, parquet_path)       # Saving Again To MINIO
        logger.info("--------------------- Data Processing & Saving Done ----------------------------")
    except AnalysisException as e:
        logger.warning(f"Can't Save To DATABASE {e}")

def main():
    
    # Initialize SparkSession with MinIO access
    logger = get_logger("Process Data")
    spark = create_spark_session("Extract and Process Crypto Data", True)

    #                      ---------------------------------------------------
    # ----- Load Currency from MinIO & Get Rate Price USD/MAD ---------
    json_path = os.getenv("MINIO_JSON_PATH")
    df = read_json_from_minio(spark, json_path) 

    flattened_df = df.select(
        col("timestamp").cast("timestamp").alias("timestamp"),
        col("bitcoin.usd").alias("BTC_usd"),
        col("ethereum.usd").alias("ETH_usd")
    )
    #                   --------------------------- To Save To DB : -------------------------
    # try:
    #     save_in_db(flattened_df, DB_TABLE = os.getenv("DB_TABLE"))    # also save to DataBase
    #     logger.info("------------- Saving To Database Done -----------")
    # except AnalysisException as e:
    #     logger.info(f"Can't save to Database {e}")

    logger.info("---------------------Starting the Data Processing ----------------------------")

    try:
        exch_api = os.getenv("EXCHANGE_API_URL")
        rate = get_rate(exch_api)
        rate_date = rate["datetime"][:10]   #.split(" ")[0]      # e.g. "2025-05-21" without time and zone
        rate_value = rate["rate"]
    except requests.exceptions.RequestException as e:
        logger.error("Can't Fetch Rate", exc_info=True)
        spark.stop()
        return
    
    # Apply Exchange Rate only if date matches

    enriched_df = flattened_df.withColumn(
        "RATE",
        when(to_date(col("timestamp")) == rate_date, rate_value)
    ).withColumn(
        "ETH_MAD",
        when(to_date(col("timestamp")) == rate_date, col("ETH_usd") * rate_value)
    ).withColumn(
        "BTC_MAD",
        when(to_date(col("timestamp")) == rate_date, col("BTC_usd") * rate_value)
    ).withColumn(
        "EXCH_time",
        when(to_date(col("timestamp")) == rate_date, rate_date)
    )

    enriched_df.filter(to_date(col("timestamp")) == rate_date).show()
    # enriched_df.show()

    save_to_minio_parquet(enriched_df, logger)

    spark.stop()



if __name__ == "__main__":
    main()