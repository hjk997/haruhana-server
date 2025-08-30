from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from routers import login
from core.logger import logger 
from routers import signup
from fastapi.middleware.cors import CORSMiddleware

ctx = ''

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

app = FastAPI()
# 라우터 등록
app.include_router(login.login_router)
app.include_router(signup.signup_router)

# 로컬에서만 허용 (포트는 프론트엔드가 띄워진 포트로 맞춰주세요)
origins = [
    "http://localhost:5500",  # 예시: VSCode Live Server
    "http://127.0.0.1:5500"
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
    # 공개 API는 통과
    if request.url.path.startswith(ctx + "/login") or request.url.path.startswith(ctx + "/signup"):
        logger.info('로그인 시도!!')
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        # ✅ 검증된 user 정보를 request.state에 저장
        request.state.user = payload
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    # 다음으로 전달
    response = await call_next(request)
    return response
