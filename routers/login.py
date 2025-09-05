from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from schemas.user import UserLogin
from crud.user import login_user
from db.database import get_db
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
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

    token = create_access_token({"user_id": user["user_id"], "user_nm": user["user_nm"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token({"user_id": user["user_id"], "user_nm": user["user_nm"]}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}

# -----------------------------
# 세션 발급 
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(tz=ZONE_INFO) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------------
# 세션 갱신
# -----------------------------
@login_router.post("/refresh")
def refresh_token(refresh_token: str = Form(...)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        user_nm = payload.get("user_nm")
        new_access_token = create_access_token(
            {"user_id": user_id, "user_nm": user_nm}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
