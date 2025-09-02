import pytest
import io
from fastapi import UploadFile
from schemas.common import ResponseMessage
from service.storage import upload_file, download_file, delete_file

# -----------------------------
# 파일 업로드
# -----------------------------
def test_upload_file():
    # given
    file_path = "test/img/default-heart.png"  # 실제 파일명으로 변경
    with open(file_path, "rb") as f:
        file_content = f.read()
    file = UploadFile(
        filename="default-heart.png",
        file=io.BytesIO(file_content),
        headers={"content-type": "image/png"}
    )
    # when
    response = upload_file('test', file)
    # then
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    assert "Upload successful" in response.message
    assert response.id is not None
    print("Uploaded file ID:", response.id)
    
    delete_result = delete_file(response.id)  # 업로드 후 파일 삭제
    assert delete_result is True
    
# -----------------------------
# 파일 다운로드
# -----------------------------
def test_upload_and_download_file():
    # given
    file_path = "test/img/default-heart.png"
    with open(file_path, "rb") as f:
        file_content = f.read()
    file = UploadFile(
        filename="default-heart.png",
        file=io.BytesIO(file_content),
        headers={"content-type": "image/png"}
    )
    # 파일 업로드
    response = upload_file('test', file)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    assert response.id is not None

    file_id = response.id
    # 파일 다운로드 테스트 (다운로드 URL 반환)
    response = download_file(file_id)
    assert 'download_url' in response
    assert isinstance(response["download_url"], str)
    assert response["download_url"].startswith("http")  # URL 형식인지 확인

    print("Download URL:", response["download_url"])
    # 실제로 다운로드 URL에 접근해서 파일이 존재하는지 확인하려면 requests 등으로 추가 테스트 가능
    # import requests
    # r = requests.get(download_url)
    # assert r.status_code == 200

    # 업로드된 파일 삭제
    delete_result = delete_file(file_id)
    assert delete_result is True