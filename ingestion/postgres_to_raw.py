import os
import pandas as pd
import psycopg2
from datetime import datetime
import boto3
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv() 

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

query = "SELECT * FROM test_connection;"
df = pd.read_sql(query, conn)

date_str = datetime.now().strftime("%Y%m%d")
file_name = f"test_connection_{date_str}.csv"
local_path = file_name

df.to_csv(local_path, index=False)



s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    config=Config(s3={'addressing_style': 'path'})
)

try:
    s3.create_bucket(Bucket="raw")
except s3.exceptions.BucketAlreadyOwnedByYou:
    pass 

s3.upload_file(
    local_path,
    "raw",
    f"postgres/test_connection/{file_name}"
)

print(f"Éxito: Archivo {file_name} subido correctamente.")