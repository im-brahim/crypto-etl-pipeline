from utils.connect import create_spark_session, get_logger
from utils.data_io import save_in_db , read_parquet_from_minio
from pyspark.sql.utils import AnalysisException # type: ignore
from utils.config import MINIO_PROCESSED_PATH , DB_TABLE_ENR

def main():
    logger = get_logger("Save New to DB")
    spark = create_spark_session("SaveNewToPostgres")

    # Step 1: Read new_data from MinIO
    try:
        df = read_parquet_from_minio(spark, MINIO_PROCESSED_PATH)
        logger.info(f"📥 Read {df.count()} new rows from new_data/")
    except AnalysisException as e:
        logger.error("❌ Failed to read new_data: " + str(e))
        spark.stop()
        return

    # Step 2: Save to PostgreSQL if data exists
    if df.count() > 0:
        # df.printSchema()
        save_in_db(df, DB_TABLE = DB_TABLE_ENR)
        logger.info(f"✅ {df.count()} New rows saved to PostgreSQL.")
    else:
        logger.info("🚫 No new rows to insert.")

    spark.stop()

if __name__ == "__main__":
    main()
