from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, aliased
from schemas.common import ResponseMessage
from models.notice import Notices
from schemas.notice import NoticeCreate, NoticeList, NoticeUpdateRead, NoticeUpdateSend, NoticeDelete
from core.logger import logger 
from sqlalchemy import func
from uuid import UUID

# -----------------------------
# 알림 목록 조회
# -----------------------------
def get_notice_list(notice_list_param: NoticeList, db: Session):
    notices = (
        db.query(Notices)
        .filter(Notices.user_id == notice_list_param.user_id, Notices.is_delete == False)
        .order_by(Notices.create_dt.desc())
        .offset(notice_list_param.skip)
        .limit(notice_list_param.limit)
        .all()
    )

    for notice in notices:
        notice.notice_id = str(notice.notice_id)
        
    return notices

def get_unread_notice_count(user_id: str, db: Session):
    count = (
        db.query(func.count(Notices.notice_id))
        .filter(Notices.user_id == user_id, Notices.is_read == False, Notices.is_delete == False)
        .scalar()
    )
    return count

# -----------------------------
# 알림 추가
# -----------------------------
def create_notice(notice: NoticeCreate, db: Session):
    new_notice = Notices(
        user_id=notice.user_id,
        notice_type=notice.notice_type,
        notice_message=notice.notice_message,
        notice_target=notice.notice_target,
        is_send=True # 추후에 알림 서비스 연동하게되면 사용하고 지금은 일단 발송상태로 저장
    )
        
    db.add(new_notice)
    try:
        db.commit()
        return ResponseMessage(code=200, message="notice created successfully", id=str(new_notice.notice_id))
    except Exception as e:
        logger.error(f"Error creating notice: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")

# -----------------------------
# 알림 발송 완료 
# -----------------------------
def send_notice(updated_notice: NoticeUpdateSend, db: Session):
    notice = (
        db.query(Notices)
        .filter(Notices.user_id == updated_notice.user_id, Notices.is_send == False)
        .all()
    )
    if not notice or len(notice) == 0:
        return ResponseMessage(code=200, message="Notice updated successfully", cnt=0)

    for n in notice:
        n.is_send = True
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notice updated successfully", cnt=len(notice))
    except Exception as e:
        logger.error(f"Error updating notice: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")

# -----------------------------
# 알림 읽기
# -----------------------------
def read_notice(updated_notice: NoticeUpdateRead, db: Session):
    notice = (
        db.query(Notices)
        .filter(Notices.notice_id == UUID(updated_notice.notice_id))
        .first()
    )
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    notice.is_read = True
    notice.read_dt = func.now()
    
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notice updated successfully")
    except Exception as e:
        logger.error(f"Error updating notice: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")

# -----------------------------
# 알림 제거
# -----------------------------
def delete_notice(deleted_notice: NoticeDelete, db: Session):
    notice = (
        db.query(Notices)
        .filter(Notices.notice_id == UUID(deleted_notice.notice_id))
        .first()
    )
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    notice.is_delete = True
    notice.delete_dt = func.now()
    
    try:
        db.commit()
        return ResponseMessage(code=200, message="Notice deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting notice: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
