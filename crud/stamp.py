from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.stamp import Stamps
from schemas.stamp import StampCreate, StampProgressUpdate, StampCompleteUpdate, StampUpdate, StampDelete
from schemas.common import ResponseMessage
from core.logger import logger 

# -----------------------------
# 스탬프 목록 조회
# -----------------------------
def get_stamp_list(user_id: str, db: Session):
    stamps = db.query(Stamps).filter(Stamps.user_id == user_id).all()
    return stamps

# -----------------------------
# 생성
# -----------------------------
def create_stamp(stamp: StampCreate, db: Session):
    new_stamp = Stamps(
        user_id=stamp.user_id,
        stamp_nm=stamp.stamp_nm,
        stamp_desc=stamp.stamp_desc,
        stamp_type=stamp.stamp_type,
        total_cnt=stamp.total_cnt,
        before_image_id=stamp.before_image_id,
        after_image_id=stamp.after_image_id
    )
    db.add(new_stamp)
    try:
        db.commit()
        return ResponseMessage(code=200, message="stamp created successfully")
    except Exception as e:
        logger.error(f"Error creating stamp: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(db_user)

# -----------------------------
# 스탬프 조회
# -----------------------------
def get_stamp(stamp_id: str, db: Session):
    stamps = db.query(Stamps).filter(Stamps.stamp_id == stamp_id).first()
    return stamps

# -----------------------------
# 수정
# -----------------------------
def update_stamp_metadata(stamp_id: str, updated_stamp: StampUpdate, db: Session):
    stamp = db.query(Stamps).filter(Stamps.stamp_id == stamp_id).first()
    if not stamp_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # dict() → model_dump(exclude_unset=True)로 변경
    for key, value in updated_stamp.model_dump(exclude_unset=True).items():
        setattr(stamp, key, value)

    try:
        db.commit()
        return ResponseMessage(code=200, message="Stamp updated successfully")
    except Exception as e:
        logger.error(f"Error updating stamp: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(user)
    
# -----------------------------
# 진행도 업데이트
# -----------------------------
def update_stamp_progress(stamp_id: str, updated_stamp: StampProgressUpdate, db: Session):
    stamp = db.query(Stamps).filter(Stamps.stamp_id == stamp_id).first()
    if not stamp_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # dict() → model_dump(exclude_unset=True)로 변경
    for key, value in updated_stamp.model_dump(exclude_unset=True).items():
        setattr(stamp, key, value)

    try:
        db.commit()
        return ResponseMessage(code=200, message="Stamp updated successfully")
    except Exception as e:
        logger.error(f"Error updating stamp: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(user)
    
# -----------------------------
# 완료 여부 업데이트
# -----------------------------
def update_stamp_complete(stamp_id: str, updated_stamp: StampCompleteUpdate, db: Session):
    stamp = db.query(Stamps).filter(Stamps.stamp_id == stamp_id).first()
    if not stamp_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # dict() → model_dump(exclude_unset=True)로 변경
    for key, value in updated_stamp.model_dump(exclude_unset=True).items():
        setattr(stamp, key, value)

    try:
        db.commit()
        return ResponseMessage(code=200, message="Stamp updated successfully")
    except Exception as e:
        logger.error(f"Error updating stamp: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(user)
    

# -----------------------------
# 삭제
# -----------------------------
def delete_stamp(stamp_id: str, deleted_stamp: StampDelete, db: Session):
    stamp = db.query(Stamps).filter(Stamps.stamp_id == stamp_id).first()
    if not stamp:
        raise HTTPException(status_code=404, detail="User not found")
    
     # dict() → model_dump(exclude_unset=True)로 변경
    for key, value in deleted_stamp.model_dump(exclude_unset=True).items():
        setattr(stamp, key, value)

    try:
        db.commit()
        return ResponseMessage(code=200, message="Stamp updated successfully")
    except Exception as e:
        logger.error(f"Error updating stamp: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(user)
   
