from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base 
from sqlalchemy.sql import func
import uuid 

class NotificationTokens(Base):
    __tablename__ = "notification_tokens"

    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    user_id = Column(String(30), ForeignKey("users.user_id"), nullable=False)  # Foreign key to users table
    token = Column(Text, nullable=False)                  # TEXT
    token_desc = Column(Text, nullable=True)              # TEXT, NULL 허용
    create_dt = Column(DateTime, nullable=True, server_default=func.current_timestamp())  # TIMESTAMP