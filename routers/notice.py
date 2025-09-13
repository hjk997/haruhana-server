from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from schemas.common import ResponseMessage
from db.database import get_db
from schemas.notice import NoticePublic, NoticeList, NoticeUpdateRead, NoticeUpdateSend, NoticeDelete
from crud.notice import get_notice_list, create_notice, delete_notice, get_unread_notice_count, read_notice, send_notice

notice_router = APIRouter(
    prefix="/notice",
    tags=["notice"]
)

# -----------------------------
# 알림 목록 조회
# -----------------------------
@notice_router.get("/list", response_model=List[NoticePublic])
def get_notice_list_route(request: Request, skip: int, limit: int, db: Session = Depends(get_db)):
    user = request.state.user
    param = NoticeList(
        user_id=user["user_id"],
        skip=skip,
        limit=limit
    )
    notices = get_notice_list(param, db=db)
    return notices

# -----------------------------
# 읽지 않은 알림 개수 조회
# -----------------------------
@notice_router.get("/unread_count")
def get_unread_notice_count_route(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    count = get_unread_notice_count(user["user_id"], db=db)
    return {"count": count}

# -----------------------------
# 알림 전송: userId를 받아서 is_send가 False인 알림들을 True로 변경
# -----------------------------
@notice_router.post("/send", response_model=ResponseMessage)
def send_notice_route(request: Request, param: NoticeUpdateSend, db: Session = Depends(get_db)):
    param.user_id = request.state.user["user_id"]
    msg = send_notice(param, db=db)
    return msg

# -----------------------------
# 알림 읽기
# -----------------------------
@notice_router.post("/read", response_model=ResponseMessage)
def read_notice_route(request: Request, param: NoticeUpdateRead, db: Session = Depends(get_db)):
    param.user_id = request.state.user["user_id"]
    msg = read_notice(param, db=db)
    return msg

# -----------------------------
# 알림 삭제
# -----------------------------
@notice_router.delete("/", response_model=ResponseMessage)
def delete_notice_route(request: Request, param: NoticeDelete, db: Session = Depends(get_db)):
    param.user_id = request.state.user["user_id"]
    msg = delete_notice(param, db=db)
    return msg