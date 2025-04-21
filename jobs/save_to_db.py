from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session with PostgreSQL driver
spark = SparkSession.builder \
    .appName("SaveToPostgres") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()
#    .config("spark.jars", "/opt/spark/jars/postgresql-42.6.0.jar") \
 
print("-------------------------------- START JOB 3 --------------------------------")
logger.info("Starting the Spark job...")


# Step 1: Read from MinIO
df = spark.read.parquet("s3a://crypto/processed/")
df.show()

# Step 2: Get latest timestamp from DB
try:
    db_df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "crypto_prices") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    max_ts = db_df.agg({"timestamp": "max"}).collect()[0][0]

    if max_ts:
        print(f"Max timestamp in DB: {max_ts}")
        df = df.filter(col("timestamp") > max_ts)

except AnalysisException:
    print("Table not found. This might be first run.")
    # Keep full df if table doesn't exist

# Step 3: Save only new rows
if df.count() > 0:
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "crypto_prices") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print("✅ New rows saved to DB.")
else:
    print("🚫 No new data to write.")

print("-------------------------------- JOB 3 is DONE --------------------------------")
logger.info("Spark job completed successfully.")

spark.stop()
