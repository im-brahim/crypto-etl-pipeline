import os
from dotenv import load_dotenv

load_dotenv()

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
        .option("url", os.getenv("DB_URL")) \
        .option("dbtable", os.getenv("DB_TABLE")) \
        .option("user", os.getenv("DB_USER")) \
        .option("password", os.getenv("DB_PASSWORD")) \
        .option("driver", os.getenv("DB_DRIVER")) \
        .load()

def save_in_db(data, DB_TABLE):
    data.write \
        .format("jdbc") \
        .option("url", os.getenv("DB_URL")) \
        .option("dbtable", DB_TABLE) \
        .option("user", os.getenv("DB_USER")) \
        .option("password", os.getenv("DB_PASSWORD")) \
        .option("driver", os.getenv("DB_DRIVER")) \
        .mode("append") \
        .save()