from datetime import datetime
from pydantic import BaseModel, Field

class FriendBase(BaseModel):
    user_id: str | None = None
    friend_user_id: str
    
    class Config:
        from_attributes = True
    
class FriendPublic(FriendBase):
    friend_user_nm: str | None = None
    friend_status: str
    
class FriendCreate(FriendBase):
    pass
    
class FriendUpdateStatus(FriendBase):
    friend_status: str
    modify_dt: str | None = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
class FriendDelete(FriendBase):
    pass