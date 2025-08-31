from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3
from botocore.client import Config
import uuid
from core.config import settings

# MinIO 설정
MINIO_ENDPOINT = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
BUCKET_NAME = settings.BUCKET_NAME

# boto3 클라이언트 생성
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4()) + "_" + file.filename
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file_id)
        return {"message": "Upload successful", "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_file(file_id: str):
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_id},
            ExpiresIn=3600,  # 1시간 유효
        )
        return {"download_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
