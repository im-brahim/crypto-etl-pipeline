from pyspark.sql import SparkSession

# Initialize SparkSession with S3 (MinIO) access
spark = SparkSession.builder \
    .appName("Read JSON from MinIO") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

print("--------------------- Starting JOB 1: ... ----------------------------")

# Read JSON data from MinIO
df = spark.read.json("s3a://crypto/crypto.json")

# Show schema and preview data
df.printSchema()
df.show(5)

# Save it temporarily for debugging (optional)
df.createOrReplaceTempView("raw_crypto")

print("---------------------- JOB 1 Done  ----------------------------")

# Stop Spark
spark.stop()
