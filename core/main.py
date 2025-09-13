from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from core.logger import logger 
from routers import login, notice, signup, stamp, stamp_image, friend, user
from fastapi.middleware.cors import CORSMiddleware
from schemas.common import ResponseMessage
from core.config import settings
ctx = ''

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

app = FastAPI()
# 라우터 등록
app.include_router(login.login_router)
app.include_router(signup.signup_router)
app.include_router(stamp.stamp_router)
app.include_router(stamp_image.stamp_image_router)
app.include_router(friend.friend_router)
app.include_router(user.user_router)
app.include_router(notice.notice_router)

# CORS 에러 처리 : 로컬에서만 허용 
origins = [
    "http://localhost:5500",  # 예시: VSCode Live Server
    "http://127.0.0.1:5500",
    settings.FRONT_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"]로 하면 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],    # 모든 HTTP 메서드 허용
    allow_headers=["*"],    # 모든 헤더 허용
)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    logger.info('진입!!')
    # OPTIONS 메서드는 인증 없이 통과
    if request.method == "OPTIONS":
        return await call_next(request)
    # 공개 API는 통과
    public_paths = ["/login", "/refresh", "/signup", "/docs", "/redoc", "/openapi.json" ]
    if any(request.url.path.startswith(ctx + path) for path in public_paths):
        logger.info('공개 API 접근: %s', request.url.path)
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        origin = request.headers.get("origin")
        headers = {}
        if origin in origins:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"
        return JSONResponse(
            status_code=200,
            content=ResponseMessage(code=401, message="Not authenticated").model_dump(),
            headers=headers
        )

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        # ✅ 검증된 user 정보를 request.state에 저장
        request.state.user = payload
    except JWTError:
        origin = request.headers.get("origin")
        headers = {}
        if origin in origins:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"
        return JSONResponse(
            status_code=200,
            content=ResponseMessage(code=401, message="Not authenticated").model_dump(),
            headers=headers
        )

    # 다음으로 전달
    response = await call_next(request)
    return response
