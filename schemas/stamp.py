from pydantic import BaseModel
from datetime import date

class StampBase(BaseModel):
    pass
    
class StampPublic(StampBase):
    stamp_id :str
    user_id : str
    stamp_nm : str 
    stamp_desc : str 
    stamp_type : str 
    total_cnt : int 
    progress_cnt : int 
    create_dt : date 
    modify_dt : date 
    complete_dt : date 
    delete_dt : date 
    isComplete : bool 
    isDelete : bool 
    
class StampCreate(StampBase):
    user_id : str 
    stamp_nm : str 
    stamp_desc : str 
    stamp_type : str 
    total_cnt : int 
    create_dt : date 

class StampUpdate(StampBase):
    stamp_nm : str 
    stamp_desc : str 
    modify_dt : date 
  
class StampProgressUpdate(StampBase):
    progress_cnt : int 
    modify_dt : date 
      
class StampCompleteUpdate(StampBase):
    progress_cnt : int 
    isComplete : bool 
    modify_dt : date 
      
class StampDelete(StampBase):
    modify_dt : date 
    delete_dt : date 
    isDelete : bool 