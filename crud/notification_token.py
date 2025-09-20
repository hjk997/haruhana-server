from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
from models.friend import Friends
from models.notification_token import NotificationTokens
from models.user import Users
from schemas.common import ResponseMessage
from core.logger import logger 

from schemas.notification_token import NotificationTokenCreate

# -----------------------------
# 알림 토큰 생성 
# -----------------------------
def create_notification_token(param: NotificationTokenCreate, db: Session):
    new_token = NotificationTokens(
        user_id=param.user_id,
        token=param.token,
        token_desc=param.token_desc
    )
    
    db.add(new_token)
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notification token created successfully")
    except Exception as e:
        logger.error(f"Error creating notification token: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    
# -----------------------------
# 알림 토큰 삭제
# -----------------------------
def delete_notification_token(token: str, db: Session):
    token = (
        db.query(NotificationTokens)
        .filter(NotificationTokens.token == token)
        .first()
    )
    if not token:
        raise HTTPException(status_code=404, detail="Notification token not found")

    db.delete(token)
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notification token deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting notification token: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    
# -----------------------------
# 알림 토큰 비활성화
# -----------------------------
def deactivate_notification_token(token: str, db: Session):
    token = (
        db.query(NotificationTokens)
        .filter(NotificationTokens.token == token)
        .first()
    )
    if not token:
        raise HTTPException(status_code=404, detail="Notification token not found")

    token.is_active = False
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notification token deactivated successfully")
    except Exception as e:
        logger.error(f"Error deactivating notification token: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    
# -----------------------------
# 유저 알림토큰 가져오기 
# -----------------------------
def get_user_notification_tokens(user_id: str, db: Session):
    tokens = (
        db.query(NotificationTokens)
        .filter(NotificationTokens.user_id == user_id, NotificationTokens.is_enabled == True)
        .all()
    )
    return tokens

# -----------------------------
# 유저 친구 알림토큰 가져오기 
# -----------------------------
def get_friend_notification_tokens(user_id: str, db: Session):
    FriendAlias = aliased(Friends)  # 별칭 생성
    tokens = (
        db.query(Friends, FriendAlias, Users)
        # Friends → Users (친구 대상 유저 정보)
        .join(Users, Friends.friend_user_id == Users.user_id)
        # Friends → Friend (셀프조인: 내가 추가한 친구 관계)
        .join(FriendAlias, Friends.user_id == FriendAlias.user_id)
        .filter(Friends.user_id == user_id and Friends.is_delete == False)
    )
    return tokens