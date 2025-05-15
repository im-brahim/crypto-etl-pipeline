from config import *

def read_json_data(spark):
    return spark.read.json(MINIO_JSON_PATH)

def read_parquet_data(spark, path):
    return spark.read.parquet(path)

def save_parquet_data(data, path):
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