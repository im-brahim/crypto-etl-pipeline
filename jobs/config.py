# Spark configuration parameters
SPARK_MASTER = "spark://master:7077"
SPARK_APP_NAME = "Crypto ETL Pipeline"

# MinIO connection parameters for Spark
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "00000000"
PATH_STYLE_ACCESS = "true"
S3A_IMPL = "org.apache.hadoop.fs.s3a.S3AFileSystem"

# MinIO storage configuration
# MINIO_JSON_BUCKET = "crypto"
# MINIO_PROCESSED_BUCKET = "crypto"
MINIO_JSON_PATH = "s3a://crypto/crypto.json"
MINIO_PARQUET_PATH = "s3a://crypto/processed/"
MINIO_PROCESSED_PATH = "s3a://tmp/new_data/"

# Database configuration
DB_URL = "jdbc:postgresql://postgres:5432/airflow"
DB_TABLE = "crypto_prices"
DB_USER = "airflow"
DB_PASSWORD = "airflow"
DB_DRIVER = "org.postgresql.Driver"

# Acces Key for API 
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"
EXCHANGE_RATE_PATH = "s3a://exchange/"