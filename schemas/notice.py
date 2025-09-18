from datetime import date
from pydantic import BaseModel, Field
from uuid import UUID

class NoticeBase(BaseModel):
    notice_id: str | None = None
    
    class Config:
        from_attributes = True

class NoticeList(NoticeBase):
    user_id: str | None = None
    skip: int = 0
    limit: int = 20

class NoticePublic(NoticeBase):
    user_id: str
    notice_type: str
    notice_message: str
    notice_target: str | None = None
    is_read: bool = False
    create_dt: date | None = None

class NoticeCreate(NoticeBase):
    user_id: str
    notice_type: str
    notice_message: str
    notice_target: str | None = None
    is_read: bool = False
    is_send: bool = False
    is_delete: bool = False
    create_dt: date | None = None

class NoticeUpdateRead(NoticeBase):
    pass

class NoticeUpdateAllRead(NoticeBase):
    user_id: str | None = None

class NoticeUpdateSend(NoticeBase):
    user_id: str | None = None

class NoticeDelete(NoticeBase):
    pass

# --- Pydantic model for incoming message data ---
class SendNotificationRequest(BaseModel):    
    token: str  # The FCM device token to send the message to
    title: str
    body: str
    data: dict = {} # Optional custom data payload
    
class NoticeTokenCreate(BaseModel):
    user_id: str | None = None
    token: str
    token_desc: str | None = None