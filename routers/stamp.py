from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from schemas.stamp import StampPublic, StampCreate, StampProgressUpdate, StampCompleteUpdate, StampUpdate, StampDelete
from schemas.common import ResponseMessage
from schemas.stamp_image import StampImageCreate
from db.database import get_db
from crud.stamp import create_stamp, get_stamp_list, update_stamp_metadata, delete_stamp, update_stamp_complete, update_stamp_progress, get_stamp
from crud.stamp_image import get_stamp_image_name_by_id
from service.storage import download_file, upload_file

stamp_router = APIRouter(
    prefix="/stamp",
    tags=["stamp"]
)

# -----------------------------
# 스탬프 목록 조회(추후 필요시 페이징 처리 추가)
# -----------------------------
@stamp_router.get("", response_model=List[StampPublic])
def get_stamp_list_route(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    stamps = get_stamp_list(user["user_id"], db=db)
    
    for stamp in stamps:
        image_key = get_stamp_image_name_by_id(stamp.after_image_id, db=db)
        response = download_file(image_key)
        if response["code"] == 200:
            stamp.image_url = response["download_url"]
    return stamps

# -----------------------------
# 스탬프 생성
# -----------------------------
@stamp_router.post("", response_model=ResponseMessage)
def create_stamp_route(request: Request, 
                       stamp_param: StampCreate, 
                       db: Session = Depends(get_db)):
    user = request.state.user
    user_id = user["user_id"]

    stamp_param.user_id = user_id

    msg = create_stamp(stamp_param, db=db)
    return msg

# -----------------------------
# 스탬프 상세 조회 (MongoDB 연동 구현 필요)
# -----------------------------
@stamp_router.get("/{stamp_id}", response_model=StampPublic)
def get_stamp_route(stamp_id: str, db: Session = Depends(get_db)):
    stamp = get_stamp(stamp_id, db=db)
    return stamp 

# -----------------------------
# 스탬프 삭제
# -----------------------------
@stamp_router.delete("/{stamp_id}", response_model=ResponseMessage)
def delete_stamp_route(stamp_id: str, stamp: StampDelete, db: Session = Depends(get_db)):
    msg = delete_stamp(stamp_id, stamp, db=db)
    return msg 

# -----------------------------
# 스탬프 진행도 업데이트
# -----------------------------
@stamp_router.put("/progress/{stamp_id}", response_model=ResponseMessage)
def update_stamp_progress_route(stamp_id: str, stamp: StampProgressUpdate, db: Session = Depends(get_db)):
    msg = update_stamp_progress(stamp, db=db)
    return msg

# -----------------------------
# 스탬프 완료 여부 업데이트
# -----------------------------
@stamp_router.put("/complete/{stamp_id}", response_model=ResponseMessage)
def update_stamp_complete_route(stamp_id: str, db: Session = Depends(get_db)):
    msg = update_stamp_complete(stamp_id, db=db)
    return msg