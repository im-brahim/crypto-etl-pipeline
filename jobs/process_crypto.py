from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, lit
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, TimestampType
import json

spark = SparkSession.builder \
    .appName("Read Crypto from MinIO") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Read the JSON file from MinIO bucket
df = spark.read.json("s3a://crypto/crypto.json")

# Show schema and data
df.printSchema()
df.show(truncate=False)

# Optional: flatten structure and show BTC/ETH prices with timestamp
df_flat = df.selectExpr("timestamp", "bitcoin.usd as bitcoin_usd", "ethereum.usd as ethereum_usd")
df_flat.show()

df_flat.write.mode("overwrite").parquet("s3a://crypto/crypto_parquet/")


# Stop Spark session
spark.stop()