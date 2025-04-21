from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime

# Initialize SparkSession with MinIO access
spark = SparkSession.builder \
    .appName("Process Crypto Data") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

print("--------------------- Starting data processing (JOB 2)... ----------------------------")

# Load JSON from MinIO
df = spark.read.json("s3a://crypto/crypto.json")

# Flatten and clean the data
flattened = df.select(
    col("timestamp").cast("timestamp").alias("timestamp"),
    col("bitcoin.usd").alias("bitcoin_usd"),
    col("ethereum.usd").alias("ethereum_usd")
)

# Show sample
flattened.show(5)
flattened.printSchema()


flattened.write.mode("overwrite").parquet("s3a://crypto/processed/")

print("--------------------- Data Processing Done ----------------------------")

spark.stop()
