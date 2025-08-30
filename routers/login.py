from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from schemas.user import UserLogin
from crud.user import login_user
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ZONE_INFO = ZoneInfo('Asia/Seoul')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

login_router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@login_router.post("")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = login_user(UserLogin(user_id= form_data.username, 
                    user_pw= form_data.password), db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": user["user_nm"]})
    return {"access_token": token, "token_type": "bearer"}

# -----------------------------
# 세션 발급 
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(tz=ZONE_INFO) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
