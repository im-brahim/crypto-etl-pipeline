from jobs.config import *

def read_json_from_minio(spark, path):
    return spark.read.json(path)

def read_parquet_from_minio(spark, path):
    return spark.read.parquet(path)

def save_json_to_minio(data, path):
    data.write.mode("overwrite").json(path)

def save_parquet_to_minio(data, path):
    data.write.mode("overwrite").parquet(path)


def read_from_db(spark):
    return spark.read \
        .format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", DB_TABLE) \
        .option("user", DB_USER) \
        .option("password", DB_PASSWORD) \
        .option("driver", DB_DRIVER) \
        .load()

def save_in_db(data):
    data.write \
        .format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", DB_TABLE) \
        .option("user", DB_USER) \
        .option("password", DB_PASSWORD) \
        .option("driver", DB_DRIVER) \
        .mode("append") \
        .save()