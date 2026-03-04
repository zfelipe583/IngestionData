import os
import json
import requests
from datetime import datetime
import boto3
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()

API_URL = "https://rickandmortyapi.com/api/character"
FUENTE_NOMBRE = "rick_and_morty_characters"

response = requests.get(API_URL)
data = response.json()["results"]   

date_str = datetime.now().strftime("%Y%m%d")
file_name = f"{FUENTE_NOMBRE}_{date_str}.json"
local_path = file_name

with open(local_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

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
    f"external/{FUENTE_NOMBRE}/{file_name}"
)

print(f"Éxito: Archivo {file_name} subido correctamente.")