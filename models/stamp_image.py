from sqlalchemy import Column, String, Boolean, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.database import Base

class StampImages(Base):
    __tablename__ = "stamp_images"

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="PK, 자동 증가")
    image_key = Column(String, nullable=False, comment="bucket 내 파일 키 (S3 또는 MinIO 경로)")
    is_public = Column(Boolean, default=True, comment="공개 여부 플래그")
    user_id = Column(String(30), ForeignKey("users.user_id"), nullable=True, comment="FK, users.user_id: 유저 전용일 시 사용")
    create_dt = Column(Date, nullable=False, comment="업로드 일자", server_default=func.current_timestamp())
    is_delete = Column(Boolean, default=False, comment="삭제 여부 플래그")
    delete_dt = Column(Date, nullable=True, comment="삭제 일자", default=None)
    image_type = Column(String(10), nullable=False, comment="이미지 유형(before, after)")
