from utils.connect import create_spark_session, get_logger
from utils.data_io import read_parquet_from_minio, read_from_db, save_parquet_to_minio
from utils.config import MINIO_PARQUET_PATH, MINIO_PROCESSED_PATH
from pyspark.sql.functions import col # type: ignore
from pyspark.sql.utils import AnalysisException # type: ignore

def main():
    logger = get_logger("Compare New Data")
    spark = create_spark_session("CompareNewData")

    # Step 1: Read processed Parquet from MinIO
    df_parquet = read_parquet_from_minio(spark, MINIO_PARQUET_PATH)
    logger.info(f"📦 Read {df_parquet.count()} rows from Parquet")

    # Step 2: Try to read DB table and get max timestamp
    try:
        df_db = read_from_db(spark)
        max_ts = df_db.agg({"timestamp": "max"}).collect()[0][0]
        logger.info(f"📌 Max timestamp in DB: {max_ts}")

        # Step 3: Filter new rows
        df_new = df_parquet.filter(col("timestamp") > max_ts)
    except AnalysisException:
        logger.info("⚠️ No existing table. Using all rows.")
        df_new = df_parquet

    # Step 4: Save new rows to new-data path
    if df_new.count() > 0:
        save_parquet_to_minio(df_new, MINIO_PROCESSED_PATH)
        logger.info(f"✅ Saved {df_new.count()} new rows to tmp/new_data/ in MINIO")
    else:
        logger.info("🚫 No new data to save.")

    spark.stop()

if __name__ == "__main__":
    main()