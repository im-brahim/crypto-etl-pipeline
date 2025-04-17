from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp


spark = SparkSession.builder \
    .appName("SaveToPostgres") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "00000000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()
#     .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
# .config("spark.jars", "/opt/spark/jars/postgresql-42.6.0.jar") \

df = spark.read.parquet("s3a://crypto/crypto_parquet/")
df.show()

# ------ Cast the timestamp column -------------
df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

############# To Save To Postgres ###################
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/airflow") \
    .option("dbtable", "crypto_prices") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

#####################################

print('************** The Data is Saving to DataBase ************')

spark.stop()
