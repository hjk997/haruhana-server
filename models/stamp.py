from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base 
import uuid

class Stamps(Base):
    __tablename__ = "stamps"

    stamp_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    user_id = Column(String(30), ForeignKey("users.user_id"), nullable=False) # FK → users.user_id
    stamp_nm = Column(String(100), nullable=False)                            # VARCHAR(100)
    stamp_desc = Column(String(200), nullable=True)                           # VARCHAR(200), NULL 허용
    stamp_type = Column(String(10), nullable=True)                            # VARCHAR(10)
    total_cnt = Column(Integer, nullable=False)                               # INT
    progress_cnt = Column(Integer, nullable=False, default=0)                 # INT DEFAULT 0
    create_dt = Column(DateTime, server_default=func.current_timestamp())         # DATE DEFAULT current_timestamp
    modify_dt = Column(DateTime, nullable=True)                                   # DATE
    complete_dt = Column(DateTime, nullable=True)                                 # DATE
    delete_dt = Column(DateTime, nullable=True)                                   # DATE
    is_complete = Column(Boolean, nullable=False, default=False)               # BOOLEAN DEFAULT FALSE
    is_delete = Column(Boolean, nullable=False, default=False)                 # BOOLEAN DEFAULT FALSE
    before_image_id = Column(UUID(as_uuid=True), ForeignKey("stamp_images.image_id"), nullable=True)  # FK → stamp_images.image_id
    after_image_id = Column(UUID(as_uuid=True), ForeignKey("stamp_images.image_id"), nullable=True)   # FK → stamp_images.image_id
