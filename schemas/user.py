from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    user_nm : str 
    user_email : str 
    
class UserPublic(UserBase):
    user_id : str 
    
class UserCreate(UserBase):
    user_id : str
    user_pw : str 

class UserUpdate(UserBase):
    user_pw : str 
    
class UserDelete(UserBase):
    delete_dt : datetime 
    is_delete : bool 
    
class UserLogin():
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
    user_id : str
    user_pw : str 