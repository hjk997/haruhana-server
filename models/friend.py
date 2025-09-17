import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db.database import Base 

class Friends(Base):
    __tablename__ = "friends"

    friend_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="PK, 자동 증가")
    user_id = Column(String(30), ForeignKey("users.user_id"), nullable=False, comment="FK, 친구 요청을 보낸 사용자")
    friend_user_id = Column(String(30), ForeignKey("users.user_id"), nullable=False, comment="FK, 친구 요청을 받은 사용자")
    friend_status = Column(String(10), default="PENDING", comment="친구 상태 (PENDING, ACCEPTED, REJECTED, RECEIVED, DELETED)")
    create_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment="생성일")
    delete_dt = Column(DateTime, nullable=True, comment="삭제일")
    is_delete = Column(Boolean, default=False, comment="삭제 여부 플래그")