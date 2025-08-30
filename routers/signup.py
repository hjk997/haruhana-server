from sqlalchemy.orm import Session
from schemas.user import UserCreate
from crud.user import create_user, check_duplicate_id, check_duplicate_email, check_duplicate_nm
from db.database import get_db
from schemas.common import ResponseMessage
from fastapi import APIRouter, Depends, HTTPException

signup_router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)

# -----------------------------
# 회원가입 
# -----------------------------
@signup_router.post("", response_model=ResponseMessage)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    # data is an instance of UserCreate, so you can access user_id as data.user_id
    # 1. 동일한 id가 있는지 확인
    if check_duplicate_id(data.user_id, db):
        raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")
    
    # 2. 동일한 email이 있는지 확인
    if check_duplicate_email(data.user_email, db):
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    
    # 3. 동일한 유저명이 있는지 확인 
    if check_duplicate_nm(data.user_nm, db):
        raise HTTPException(status_code=400, detail="이미 사용 중인 유저명입니다.")
    
    # fin. 사용자 생성
    result = create_user(data, db=db)
    
    return result