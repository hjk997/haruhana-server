from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import Users  # SQLAlchemy ORM 모델
from schemas.user import UserBase, UserUpdate, UserCreate, UserDelete, UserLogin
from schemas.common import ResponseMessage
from passlib.context import CryptContext
from core.logger import logger 

pwcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# -----------------------------
# 유저 목록 조회
# -----------------------------
def get_user_list(query: str, db: Session):
    users = db.query(Users).filter(
        (
            (Users.user_id.contains(query)) | 
            (Users.user_nm.contains(query)) 
        ) & (Users.is_delete == False)
    ).all()
    return users

# -----------------------------
# 조회
# -----------------------------
def get_user(user_id: str, db: Session):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -----------------------------
# 생성
# -----------------------------
def create_user(user_create: UserCreate, db: Session):
    db_user = Users(
        user_id=user_create.user_id,
        user_pw=pwcrypt_context.hash(user_create.user_pw),
        user_nm=user_create.user_nm,
        user_email=user_create.user_email
    )
    db.add(db_user)
    try:
        db.commit()
        return ResponseMessage(code=200, message="User created successfully")
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(db_user)


# -----------------------------
# 중복 id 확인  
# -----------------------------
def check_duplicate_id(user_id: str, db: Session):
    existing_user = db.query(Users).filter(Users.user_id == user_id).first()
    if existing_user:
        return True
    return False

# -----------------------------
# 중복 유저명 확인  
# -----------------------------
def check_duplicate_nm(user_nm: str, db: Session):
    existing_user = db.query(Users).filter(Users.user_nm == user_nm).first()
    if existing_user:
        return True
    return False

# -----------------------------
# 중복 이메일 확인  
# -----------------------------
def check_duplicate_email(user_email: str, db: Session):
    existing_user = db.query(Users).filter(Users.user_email == user_email).first()
    if existing_user:
        return True
    return False

# -----------------------------
# 수정
# -----------------------------
def update_user(user_id: str, updated_user: UserUpdate, db: Session):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # pw 암호화 
    updated_user.user_pw = pwcrypt_context.hash(updated_user.user_pw)
    
    # dict() → model_dump(exclude_unset=True)로 변경
    for key, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        db.commit()
        return ResponseMessage(code=200, message="User updated successfully")
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(user)
    

# -----------------------------
# 삭제
# -----------------------------
def delete_user(user_id: str, db: Session):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    try:
        db.commit()
        return ResponseMessage(code=200, message="User deleted successfully")
    except Exception as e:
        logger.error(f"Error delete user: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
   # return {"detail": "User deleted successfully"}
   
# -----------------------------
# 로그인 
# -----------------------------
def login_user(user_login: UserLogin, db: Session):
    user = db.query(Users).filter(Users.user_id == user_login.user_id and Users.user_pw == user_login.user_pw).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return {"user_id": user.user_id, "user_nm": user.user_nm}
    
    