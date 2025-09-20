from datetime import date
from pydantic import BaseModel, Field
from uuid import UUID

class NotificationToken(BaseModel):
    class Config:
        from_attributes = True

# --- Pydantic model for incoming message data ---
class SendNotificationRequest(NotificationToken):    
    token: str
    title: str
    body: str
    data: dict = {} # Optional custom data payload
    
class NotificationTokenCreate(NotificationToken):
    token: str
    user_id: str | None = None
    token_desc: str | None = None
    
class NotificationTokenSelect(NotificationToken):
    user_id: str | None = None
    