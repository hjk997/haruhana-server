from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, Form
from sqlalchemy.orm import Session
from schemas.stamp_image import StampImagePublic, StampImageCreate, StampImageDelete
from schemas.common import ResponseMessage
from db.database import get_db
from crud.stamp_image import get_stamp_image_list, create_stamp_image, delete_stamp_image
from service.storage import upload_file, download_file

stamp_image_router = APIRouter(
    prefix="/stamp-image",
    tags=["stamp-image"]
)

# -----------------------------
# 스탬프 이미지 목록 조회
# -----------------------------
@stamp_image_router.get("", response_model=List[StampImagePublic])
def get_stamp_image_list_route(request: Request, image_type: str, db: Session = Depends(get_db)):
    user = request.state.user
    # SQLAlchemy 객체 → Pydantic 모델로 변환
    stamp_images = get_stamp_image_list(user["user_id"], image_type=image_type, db=db)
    for img in stamp_images:
        response = download_file(img.image_key)
        if response["code"] == 200:
            img.image_key = response["download_url"]
    return [StampImagePublic.model_validate(img) for img in stamp_images]


# -----------------------------
# 스탬프 이미지 추가
# -----------------------------
@stamp_image_router.put("", response_model=ResponseMessage)
def insert_stamp_image_route(request: Request, file: UploadFile, image_type: str = Form(...), is_public: str = Form(...), db: Session = Depends(get_db)): 
    user = request.state.user
    
    # 파일 확장자 추출하기 
    file_ext = file.filename.split(".")[-1]
    if file_ext.lower() not in ["jpg", "jpeg", "png", "gif", "bmp"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image file.")
    
    # 파일 업로드 처리 (예: S3에 업로드)
    upload_response = upload_file(user["user_id"], file)
    print(upload_response.code)
    if upload_response.code != 200:
        raise HTTPException(status_code=500, detail="File upload failed.")
    
    # DB 업로드 처리 
    stamp_param = StampImageCreate(
        user_id = user["user_id"],
        image_key=upload_response.id,
        image_type=image_type,
        is_public=is_public
    )
    
    result = create_stamp_image(stamp_param, db=db)
    return result
    

# -----------------------------
# 스탬프 이미지 삭제
# -----------------------------
@stamp_image_router.delete("/", response_model=ResponseMessage)
def delete_stamp_image_route(param: StampImageDelete, db: Session = Depends(get_db)):
    result = delete_stamp_image(param, db=db)
    return result
    
