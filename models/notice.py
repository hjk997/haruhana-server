import uuid
from sqlalchemy import Column, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db.database import Base

class Notices(Base):
    __tablename__ = "notices"

    notice_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="PK")
    user_id = Column(String(30), ForeignKey("users.user_id"), nullable=False, comment="FK, 알림 대상 유저")
    notice_type = Column(String(20), nullable=False, comment="알림 타입")
    notice_message = Column(Text, nullable=False, comment="알림 메시지")
    is_read = Column(Boolean, default=False, comment="읽음 여부")
    is_send = Column(Boolean, default=False, comment="발송 여부")
    is_delete = Column(Boolean, default=False, comment="삭제 여부")
    create_dt = Column(Date, nullable=False, server_default=func.current_timestamp(), comment="생성일")
    read_dt = Column(Date, nullable=True, comment="읽은 일자")
    delete_dt = Column(Date, nullable=True, comment="삭제 일자")
    notice_target = Column(String(30), nullable=True, comment="알림 대상 (예: 친구 요청을 보낸 사용자 ID)")