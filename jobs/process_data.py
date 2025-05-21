from jobs.connect import create_spark_session, get_logger
from jobs.data_io import read_json_from_minio, save_parquet_to_minio, read_parquet_from_minio
from pyspark.sql.functions import col, to_date, when
from jobs.config import MINIO_PARQUET_PATH , MINIO_JSON_PATH, EXCHANGE_API_URL
from jobs.scripts.rate import get_rate
from pyspark.errors import AnalysisException

# Initialize SparkSession with MinIO access
logger = get_logger("Process Data")
spark = create_spark_session("Extract and Process Crypto Data")

#                      ---------------------------------------------------
# ----- Load Currency from MinIO & Get Rate Price USD/MAD ---------
df = read_json_from_minio(spark, MINIO_JSON_PATH) 

try:
    rate = get_rate(EXCHANGE_API_URL)
    rate_date = rate["datetime"][:10]   #.split(" ")[0]      # e.g. "2025-05-21" without time and zone
    rate_value = rate["rate"]
except:
    logger.info("Can't Fetch Rate")
    spark.stop()

logger.info("---------------------Starting the Data Processing ----------------------------")

flattened_df = df.select(
    col("timestamp").cast("timestamp").alias("timestamp"),
    col("bitcoin.usd").alias("BTC_usd"),
    col("ethereum.usd").alias("ETH_usd")
)

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

# Save all the Data to MINIO
try:
    save_parquet_to_minio(enriched_df, MINIO_PARQUET_PATH)       # Saving Again To MINIO
    logger.info("--------------------- Data Processing & Saving Done ----------------------------")
except AnalysisException as e:
    logger.warning(f"Can't Save To DATABASE {e}")

spark.stop()
