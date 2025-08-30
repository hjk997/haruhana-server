from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User  # ORM 모델
from schemas.user import UserCreate, UserUpdate, UserPublic
from schemas.common import ResponseMessage
from db.database import get_db
from crud.user import create_user, get_user, update_user, delete_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# -----------------------------
# 전체 사용자 조회 : 필요없는데 참고용으로 남겨둠 
# -----------------------------
#@router.get("/", response_model=List[UserRead])
#def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = db.query(User).offset(skip).limit(limit).all()
#    return users

# -----------------------------
# 단일 사용자 조회
# -----------------------------
@router.get("/{user_id}", response_model=UserPublic)
def read_user_route(user_id: str, db: Session = Depends(get_db)):
    user = get_user(user_id, db=db)

# -----------------------------
# 사용자 생성
# -----------------------------
@router.post("/", response_model=ResponseMessage)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    msg = create_user(user, db=db)
    return msg

# -----------------------------
# 사용자 수정
# -----------------------------
@router.put("/{user_id}", response_model=ResponseMessage)
def update_user_route(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    msg = update_user(user_id, user, db=db)
    return msg

# -----------------------------
# 사용자 삭제
# -----------------------------
@router.delete("/{user_id}", response_model=ResponseMessage)
def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    msg = delete_user(user_id, db=db)
    return msg 
