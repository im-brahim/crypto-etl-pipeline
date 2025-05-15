from pyspark.sql import SparkSession
import logging
from config import *

def get_logger(name):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

def create_spark_session(app_name=SPARK_APP_NAME):
    """Create a Spark session with appropriate configurations"""
    builder = SparkSession.builder \
        .appName(app_name) \
        .master(SPARK_MASTER) \
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT) \
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.path.style.access", PATH_STYLE_ACCESS) \
        .config("spark.hadoop.fs.s3a.impl", S3A_IMPL) \
    
    return builder.getOrCreate()
    