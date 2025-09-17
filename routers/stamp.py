from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from schemas.stamp import StampPublic, StampCreate, StampProgressUpdate, StampCompleteUpdate, StampUpdate, StampDelete
from schemas.common import ResponseMessage
from schemas.stamp_image import StampImageCreate
from db.database import get_db
from crud.stamp import create_stamp, get_stamp_list, update_stamp_metadata, delete_stamp, update_stamp_complete, update_stamp_progress, get_stamp
from crud.stamp_image import get_stamp_image_name_by_id
from schemas.stamp_record import StampRecordUpdate
from service.storage import download_file
from crud.stamp_record import find_stamp_record, init_stamp_record, update_stamp_record

stamp_router = APIRouter(
    prefix="/stamp",
    tags=["stamp"]
)

# -----------------------------
# 스탬프 목록 조회(추후 필요시 페이징 처리 추가)
# -----------------------------
@stamp_router.get("/list", response_model=List[StampPublic])
def get_stamp_list_route(request: Request, is_complete: str, db: Session = Depends(get_db)):
    user = request.state.user
    stamps = get_stamp_list(user["user_id"], (is_complete == "Y" if True else False), db=db)

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

    # db에 스탬프 생성 
    msg = create_stamp(stamp_param, db=db)
    
    if(msg.code == 200):
        # MongoDB에 스탬프 정보 초기화
        init_stamp_record(msg.id, stamp_param.total_cnt)
        
    return msg

# -----------------------------
# 스탬프 상세 조회 
# -----------------------------
@stamp_router.get("", response_model=StampPublic)
def get_stamp_route(stamp_id: str, db: Session = Depends(get_db)):
    stamp = get_stamp(stamp_id, db=db)

    before_response = download_file(get_stamp_image_name_by_id(stamp.before_image_id, db=db))
    if before_response["code"] == 200:
        stamp.before_image_url = before_response["download_url"]
    after_response = download_file(get_stamp_image_name_by_id(stamp.after_image_id, db=db))
    if after_response["code"] == 200:
        stamp.after_image_url = after_response["download_url"]
    return stamp

# -----------------------------
# 스탬프 요소 별 상세 조회 
# -----------------------------
@stamp_router.get("/record")
def get_stamp_record_route(stamp_id: str):
    stamp_record = find_stamp_record(stamp_id)
    if "_id" in stamp_record and isinstance(stamp_record["_id"], ObjectId):
        stamp_record["_id"] = str(stamp_record["_id"])
    return stamp_record

# -----------------------------
# 스탬프 삭제
# -----------------------------
@stamp_router.delete("", response_model=ResponseMessage)
def delete_stamp_route(param: StampDelete, db: Session = Depends(get_db)):
    msg = delete_stamp(param, db=db)
    return msg 

# -----------------------------
# 스탬프 진행도 업데이트
# -----------------------------
@stamp_router.put("/progress", response_model=ResponseMessage)
def update_stamp_progress_route(stamp: StampRecordUpdate, db: Session = Depends(get_db)):
    # 1. record 업데이트 
    stamp_id = stamp.stamp_id
    update_stamp_record(stamp_id, stamp)
    
    # 2. db 업데이트 
    msg = update_stamp_progress(stamp_id, stamp.progress_cnt, db=db)
    return msg

# -----------------------------
# 스탬프 완료 여부 업데이트
# -----------------------------
@stamp_router.put("/complete", response_model=ResponseMessage)
def update_stamp_complete_route(stamp_id: str, db: Session = Depends(get_db)):
    msg = update_stamp_complete(stamp_id, db=db)
    return msg