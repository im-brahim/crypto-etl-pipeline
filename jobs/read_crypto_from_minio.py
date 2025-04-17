from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = SparkSession.builder \
    .appName("Read Crypto from MinIO") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Read the file as text
df_raw = spark.read.text("s3a://crypto/crypto.json")

# Define schema for one record
schema = StructType([
    StructField("bitcoin", StructType([
        StructField("usd", DoubleType())
    ])),
    StructField("ethereum", StructType([
        StructField("usd", DoubleType())
    ])),
    StructField("timestamp", StringType())
])

# Parse each line to JSON
df = df_raw.select(from_json(col("value"), schema).alias("data")).select("data.*")

df.show(truncate=False)

spark.stop()
