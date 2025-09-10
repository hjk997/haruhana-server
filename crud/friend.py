from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, aliased
from schemas.common import ResponseMessage
from models.friend import Friends
from models.user import Users
from schemas.friend import FriendCreate, FriendUpdateStatus, FriendPublic, FriendDelete
from core.logger import logger 
from sqlalchemy import func

# -----------------------------
# 친구 목록 조회
# -----------------------------
def get_friend_list(user_id: str, status: str, db: Session):
    # Friends 테이블을 self join하여 친구의 user 정보까지 가져오기
    FriendAlias = aliased(Friends)  # 별칭 생성
    friends = (
        db.query(Friends, FriendAlias, Users)
        # Friends → Users (친구 대상 유저 정보)
        .join(Users, Friends.friend_user_id == Users.user_id)
        # Friends → Friend (셀프조인: 내가 추가한 친구 관계)
        .join(FriendAlias, Friends.user_id == FriendAlias.user_id)
        .filter(Friends.user_id == user_id and Friends.is_delete == False)
    )
    
    if status == "ALL":
        friends = friends.filter(Friends.friend_status != 'REJECTED')
    elif status == "PENDING":
        friends = friends.filter(Friends.friend_status == 'PENDING')
    # 필요하다면 ACCEPTED 등 다른 조건도 추가 가능

    friends = friends.order_by(Friends.create_dt.desc()).all()

    friend_list = []
    for ele in friends:
        friend_info = FriendPublic(
            friend_id=str(ele.Friends.friend_id),
            user_id=ele.Friends.user_id,
            friend_user_id=ele.Friends.friend_user_id,
            friend_status=ele.Friends.friend_status,
            create_dt=ele.Friends.create_dt,
            delete_dt=ele.Friends.delete_dt,
            is_delete=ele.Friends.is_delete,
            friend_user_nm=ele.Users.user_nm,
            friend_user_email=ele.Users.user_email
        )
        print(friend_info)
        friend_list.append(friend_info)
    return friend_list

# -----------------------------
# 친구 요청 추가
# -----------------------------
def create_friend(friend: FriendCreate, db: Session):
    new_friend1 = Friends(
        user_id=friend.user_id,
        friend_user_id=friend.friend_user_id,
        friend_status="PENDING"
    )
    new_friend2 = Friends(
        user_id=friend.friend_user_id,
        friend_user_id=friend.user_id,
        friend_status="PENDING"
    )
    db.add_all([new_friend1, new_friend2])
    try:
        db.commit()
        return ResponseMessage(code=200, message="friend created successfully", id=str(new_friend1.friend_id))
    except Exception as e:
        logger.error(f"Error creating friend: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
    #db.refresh(db_user)

# -----------------------------
# 친구 상태 수정
# -----------------------------
def update_friend_status(updated_friend: FriendUpdateStatus, db: Session):
    # 두 방향의 친구 관계를 모두 조회
    friends = db.query(Friends).filter(
        ((Friends.user_id == updated_friend.user_id) & (Friends.friend_user_id == updated_friend.friend_user_id)) |
        ((Friends.user_id == updated_friend.friend_user_id) & (Friends.friend_user_id == updated_friend.user_id))
    ).all()
    if len(friends) != 2:
        raise HTTPException(status_code=404, detail="Friend relationship not found")

    for friend in friends:
        friend.friend_status = updated_friend.friend_status

    try:
        db.commit()
        return ResponseMessage(code=200, message="Friend updated successfully")
    except Exception as e:
        logger.error(f"Error updating friend: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")

# -----------------------------
# 삭제
# -----------------------------
def delete_friend(deleted_friend: FriendDelete, db: Session):
    friends = db.query(Friends).filter(
        ((Friends.user_id == deleted_friend.user_id) & (Friends.friend_user_id == deleted_friend.friend_user_id)) |
        ((Friends.user_id == deleted_friend.friend_user_id) & (Friends.friend_user_id == deleted_friend.user_id))
    ).all()
    if len(friends) != 2:
        raise HTTPException(status_code=404, detail="Friend relationship not found")

    for friend in friends:
        friend.is_delete = True
        friend.delete_dt = func.now()
        
    try:
        db.commit()
        return ResponseMessage(code=200, message="Friend deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting friend: {str(e)}")
        db.rollback()
        return ResponseMessage(code=500, message=f"Error: {str(e)}")
   
