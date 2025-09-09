from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from schemas.common import ResponseMessage
from db.database import get_db
from schemas.friend import FriendPublic, FriendCreate, FriendUpdateStatus, FriendDelete
from crud.friend import get_friend_list, create_friend, delete_friend, update_friend_status

friend_router = APIRouter(
    prefix="/friend",
    tags=["friend"]
)

# -----------------------------
# 친구 목록 조회(추후 필요시 페이징 처리 추가)
# -----------------------------
@friend_router.get("/list", response_model=List[FriendPublic])
def get_friend_list_route(request: Request, is_complete: str, db: Session = Depends(get_db)):
    user = request.state.user
    friends = get_friend_list(user["user_id"], db=db)

    return friends

# -----------------------------
# 스탬프 생성
# -----------------------------
@friend_router.post("", response_model=ResponseMessage)
def create_friend_route(request: Request, friend: FriendCreate, db: Session = Depends(get_db)):
    # db에 친구 생성
    msg = create_friend(friend, db=db)
    
    return msg

# -----------------------------
# 친구 삭제
# -----------------------------
@friend_router.delete("", response_model=ResponseMessage)
def delete_friend_route(friend: FriendDelete, db: Session = Depends(get_db)):
    msg = delete_friend(friend, db=db)
    return msg

# -----------------------------
# 친구 상태 업데이트
# -----------------------------
@friend_router.put("/status", response_model=ResponseMessage)
def update_friend_status_route(friend: FriendUpdateStatus, db: Session = Depends(get_db)):
    msg = update_friend_status(friend, db=db)
    return msg