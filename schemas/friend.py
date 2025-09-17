from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import func

from schemas.user import UserPublic

class FriendBase(BaseModel):
    user_id: str | None = None
    friend_user_id: str
    
    class Config:
        from_attributes = True
    
class UserSearch(UserPublic):
    friend_status: str | None = None
    
class FriendPublic(FriendBase):
    friend_user_nm: str | None = None
    friend_status: str
    
class FriendCreate(FriendBase):
    pass
    
class FriendUpdateStatus(FriendBase):
    friend_status: str
    modify_dt: str | None = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
class FriendDelete(FriendBase):
    pass