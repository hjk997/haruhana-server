from datetime import datetime
from pydantic import BaseModel, Field

class FriendBase(BaseModel):
    class Config:
        from_attributes = True
    
class FriendPublic(FriendBase):
    user_id: str
    friend_user_id: str
    friend_user_nm: str | None = None
    friend_status: str
    
class FriendCreate(FriendBase):
    user_id: str
    friend_user_id: str
    friend_status: str
    
class FriendUpdateStatus(FriendBase):
    user_id: str
    friend_user_id: str
    friend_status: str
    modify_dt: str | None = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
class FriendDelete(FriendBase):
    user_id: str
    friend_user_id: str