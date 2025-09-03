from pydantic import BaseModel
from datetime import date
from uuid import UUID

class StampImageBase(BaseModel):
    image_key : str| None = None
    is_public : bool 
    image_type: str
    
    class Config:
        from_attributes = True
    
class StampImagePublic(StampImageBase):
    image_id : UUID 
    
class StampImageCreate(StampImageBase):
    user_id : str | None = None

class StampImageDelete(BaseModel):
    is_delete: bool
    delete_dt: date | None = None