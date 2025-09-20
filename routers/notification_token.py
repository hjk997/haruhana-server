from fastapi import Depends, Request
from sqlalchemy.orm import Session
from schemas.common import ResponseMessage
from db.database import get_db
from crud.notice import create_notification_token
from schemas.notification_token import NotificationTokenCreate
from routers.notice import notice_router

# -----------------------------
# 사용자 알림 토큰 추가
# -----------------------------
@notice_router.post("/token", response_model=ResponseMessage)
def create_notification_token_route(request: Request, param: NotificationTokenCreate, db: Session = Depends(get_db)):
    param.user_id = request.state.user["user_id"]
    msg = create_notification_token(param, db=db)
    return msg