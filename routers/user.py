from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from urllib3 import request
from schemas.user import UserCreate, UserUpdate, UserPublic
from schemas.common import ResponseMessage
from db.database import get_db
from crud.user import get_user_list, get_user, update_user, delete_user

user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

# -----------------------------
# 사용자 조회 
# -----------------------------
@user_router.get("/list", response_model=List[UserPublic])
def get_user_list_route(request: Request, query: str, db: Session = Depends(get_db)):
    user = request.state.user
    users = get_user_list(query, user["user_id"], db=db)
    return users

# -----------------------------
# 단일 사용자 조회
# -----------------------------
@user_router.get("/{user_id}", response_model=UserPublic)
def read_user_route(user_id: str, db: Session = Depends(get_db)):
    user = get_user(user_id, db=db)

# -----------------------------
# 사용자 수정
# -----------------------------
@user_router.put("/{user_id}", response_model=ResponseMessage)
def update_user_route(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    msg = update_user(user_id, user, db=db)
    return msg

# -----------------------------
# 사용자 삭제
# -----------------------------
@user_router.delete("/{user_id}", response_model=ResponseMessage)
def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    msg = delete_user(user_id, db=db)
    return msg 
