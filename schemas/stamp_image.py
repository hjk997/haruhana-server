from pydantic import BaseModel
from datetime import date
from uuid import UUID

class StampImageBase(BaseModel):
    class Config:
        from_attributes = True
    
class StampImagePublic(StampImageBase):
    image_id : UUID 
    image_key : str | None = None
    is_public : bool 
    image_type: str
    
class StampImageCreate(StampImageBase):
    user_id : str | None = None
    image_key : str | None = None
    is_public : bool 
    image_type: str

class StampImageDelete(StampImageBase):
    image_id : str