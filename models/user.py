from sqlalchemy import Column, DateTime, Integer, String, Date, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base 
import uuid

class Users(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    user_id = Column(String(30), unique=True, index=True, nullable=False)                # VARCHAR(50)
    user_nm = Column(String(30), nullable=False)                  # VARCHAR(30)
    user_email = Column(String(50), nullable=False)               # VARCHAR(50)
    user_pw = Column(String(60), nullable=False)                  # VARCHAR(50)
    create_dt = Column(DateTime, nullable=True, server_default=func.current_timestamp())                       # DATE
    delete_dt = Column(DateTime, nullable=True)                       # DATE, NULL 허용
    is_delete = Column(Boolean, nullable=False, default=False)     # BOOLEAN
