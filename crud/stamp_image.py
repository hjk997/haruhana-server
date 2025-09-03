from fastapi import Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from models.stamp_image import StampImages
from schemas.stamp_image import StampImagePublic, StampImageCreate, StampImageDelete
from schemas.common import ResponseMessage
from core.logger import logger 

# -----------------------------
# 스탬프 이미지 목록 조회
# -----------------------------
def get_stamp_image_list(user_id: str, image_type: str, db: Session):
    stamps_public = db.query(StampImages).filter(
        and_(
            StampImages.is_public == True , 
            StampImages.image_type == image_type,
            StampImages.is_delete == False
        )
        ).all()
    stamps_user = db.query(StampImages).filter(
        and_(
            StampImages.user_id == user_id, 
            StampImages.image_type == image_type,
            StampImages.is_delete == False
        )
        ).all()
    stamp_images = stamps_user + stamps_public
    
    return stamp_images

# -----------------------------
# 스탬프 key 조회
# -----------------------------
def get_stamp_image_name_by_id(image_id: str, db: Session):
    stamp_image = db.query(StampImages).filter(StampImages.image_id == image_id).first()
    if not stamp_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return stamp_image.image_key

# -----------------------------
# 생성
# -----------------------------
def create_stamp_image(stamp_image: StampImageCreate, db: Session):
    new_stamp_image = StampImages(
        image_key=stamp_image.image_key,
        is_public=stamp_image.is_public,
        user_id=stamp_image.user_id,
        image_type=stamp_image.image_type
    )
    db.add(new_stamp_image)
    try:
        db.commit()
        return ResponseMessage(code=200, message="stamp image created successfully", id=str(new_stamp_image.image_id))
    except Exception as e:
        logger.error(f"Error creating stamp image: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")


# -----------------------------
# 삭제
# -----------------------------
def delete_stamp_image(image_id: str, db: Session):
    stamp_image = db.query(StampImages).filter(StampImages.image_id == image_id).first()
    if not stamp_image:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(stamp_image)
    try:
        db.commit()
        return ResponseMessage(code=200, message="Stamp image deleted successfully")
    except Exception as e:
        logger.error(f"Error delete stamp image: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
   
