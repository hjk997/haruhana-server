from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from schemas.common import ResponseMessage
from db.database import get_db
from schemas.friend import FriendPublic, FriendCreate, FriendUpdateStatus, FriendDelete, UserSearch
from crud.friend import get_friend_list, create_friend, delete_friend, get_user_with_friend_info_list, update_friend_status
from crud.notice import create_notice
from schemas.notice import NoticeCreate

friend_router = APIRouter(
    prefix="/friend",
    tags=["friend"]
)

# -----------------------------
# 친구 목록 조회(추후 필요시 페이징 처리 추가)
# -----------------------------
@friend_router.get("/list", response_model=List[FriendPublic])
def get_friend_list_route(request: Request, status: str, db: Session = Depends(get_db)):
    user = request.state.user
    friends = get_friend_list(user["user_id"], status=status, db=db)
    return friends

# -----------------------------
# 친구 생성
# -----------------------------
@friend_router.post("", response_model=ResponseMessage)
def create_friend_route(request: Request, friend: FriendCreate, db: Session = Depends(get_db)):
    # 1. db에 친구 생성
    friend.user_id = request.state.user["user_id"]
    msg = create_friend(friend, db=db)
    
    if msg.code != 200:
        return msg
    
    # 2. 친구 요청 알림 추가 
    notice = NoticeCreate(
        user_id=friend.friend_user_id,
        notice_type="friend_request",
        notice_message=f"{request.state.user['user_nm']}님이 친구 요청을 보냈습니다.",
        notice_target=friend.user_id
    )
    msg = create_notice(notice, db=db)

    return msg

# -----------------------------
# 친구 삭제
# -----------------------------
@friend_router.delete("", response_model=ResponseMessage)
def delete_friend_route(request: Request, friend: FriendDelete, db: Session = Depends(get_db)):
    friend.user_id = request.state.user["user_id"]
    msg = delete_friend(friend, db=db)
    return msg

# -----------------------------
# 친구 상태 업데이트
# -----------------------------
@friend_router.put("/status", response_model=ResponseMessage)
def update_friend_status_route(request: Request, friend: FriendUpdateStatus, db: Session = Depends(get_db)):
    friend.user_id = request.state.user["user_id"]
    msg = update_friend_status(friend, db=db)
    return msg

# -----------------------------
# 유저 검색(친구 상태 포함)
# -----------------------------
@friend_router.get("/searchuser", response_model=List[UserSearch])
def get_user_with_friend_info_list_route(request: Request, query: str, db: Session = Depends(get_db)):
    user = request.state.user
    users = get_user_with_friend_info_list(query, user["user_id"], db)
    return users