from pydantic import BaseModel
from datetime import date
from uuid import UUID
from sqlalchemy import func

class StampBase(BaseModel):
    class Config:
        from_attributes = True
    
class StampPublic(StampBase):
    stamp_id :UUID
    user_id : str
    stamp_nm : str 
    stamp_desc : str 
    stamp_type : str 
    total_cnt : int 
    progress_cnt : int 
    create_dt : date | None = None
    modify_dt : date | None = None
    complete_dt : date | None = None
    delete_dt : date | None = None
    is_complete : bool 
    is_delete : bool 
    before_image_id : UUID | None = None
    after_image_id : UUID | None = None
    before_image_url: str | None = None
    after_image_url: str | None = None
    image_url: str | None = None

class StampCreate(StampBase):
    user_id : str | None = None
    stamp_nm : str 
    stamp_desc : str    
    stamp_type : str 
    total_cnt : int 
    create_dt : date | None = None
    before_image_id : str
    after_image_id : str 

class StampUpdate(StampBase):
    stamp_nm : str 
    stamp_desc : str 
    modify_dt : date 
  
class StampProgressUpdate(StampBase):
    def __init__(self, progress_cnt: int):
        self.progress_cnt = progress_cnt
        self.modify_dt = func.now()

    progress_cnt : int 
    modify_dt : date 
      
class StampCompleteUpdate(StampBase):
    progress_cnt : int 
    is_complete : bool 
    modify_dt : date 
      
class StampDelete(StampBase):
    modify_dt : date 
    delete_dt : date 
    is_delete : bool 