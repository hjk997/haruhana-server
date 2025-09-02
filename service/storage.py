from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3
from botocore.client import Config
import uuid
from core.config import settings
from schemas.common import ResponseMessage

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

def upload_file(user_id: str, file: UploadFile = File(...)):
    """
    파일(오브젝트) 업로드
    :param user_id: 사용자 ID
    :param file: 업로드할 파일
    :return: 업로드 결과 메시지
    """
    try:
        file_id = str(uuid.uuid4()) + "_" + user_id
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file_id)
        return ResponseMessage(code="200", message="Upload successful", id=file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_file(file_id: str):
    """
    파일(오브젝트) 다운로드
    :param file_id: 다운로드할 파일의 key 또는 경로
    :return: 다운로드 URL 또는 오류 메시지
    """
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_id},
            ExpiresIn=3600,  # 1시간 유효
        )
        return {"download_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_file(object_name: str):
    """
    파일(오브젝트) 삭제
    :param object_name: 삭제할 파일의 key 또는 경로
    :return: True(성공) 또는 False(실패)
    """
    bucket_name = BUCKET_NAME

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        return True
    except Exception as e:
        # 필요시 로깅
        print(f"MinIO 파일 삭제 오류: {e}")
        return False