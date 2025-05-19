from connect import create_spark_session, get_logger
from data_io import read_json_from_minio, save_parquet_to_minio 
from pyspark.sql.functions import col # type: ignore
from config import MINIO_PARQUET_PATH , MINIO_JSON_PATH


def process_data(df):
    flattened = df.select(
        col("timestamp").cast("timestamp").alias("timestamp"),
        col("bitcoin.usd").alias("bitcoin_usd"),
        col("ethereum.usd").alias("ethereum_usd")
    )
    return flattened


def main():
    # Initialize SparkSession with MinIO access
    logger = get_logger("Process Data")
    spark = create_spark_session("Extract and Process Crypto Data")

    # ----- Load JSON from MinIO ---------
    df = read_json_from_minio(spark, MINIO_JSON_PATH)

    # ----- Show schema and preview data ---------
    # df.printSchema()
    # df.show(5)

    logger.info("--------------------- Starting data processing... -------------------------------")
    
    processed_data = process_data(df)
    # processed_data.show(5)

    save_parquet_to_minio(processed_data, MINIO_PARQUET_PATH)       # Saving Again To MINIO
    logger.info("--------------------- Data Processing & Saving Done ----------------------------")

    spark.stop()


if __name__ == "__main__":
    main()