from connect import create_spark_session, get_logger
from data_io import save_in_db , read_parquet_from_minio
from pyspark.sql.utils import AnalysisException # type: ignore
from config import MINIO_PROCESSED_PATH

def main():
    logger = get_logger("Save New to DB")
    spark = create_spark_session("SaveNewToPostgres")

    # Step 1: Read new_data from MinIO
    try:
        df_new = read_parquet_from_minio(spark, MINIO_PROCESSED_PATH)
        logger.info(f"📥 Read {df_new.count()} new rows from new_data/")
    except AnalysisException as e:
        logger.error("❌ Failed to read new_data: " + str(e))
        spark.stop()
        return

    # Step 2: Save to PostgreSQL if data exists
    if df_new.count() > 0:
        save_in_db(df_new)
        logger.info(f"✅ {df_new.count()} New rows saved to PostgreSQL.")
    else:
        logger.info("🚫 No new rows to insert.")

    spark.stop()

if __name__ == "__main__":
    main()
