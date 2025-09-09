import pytest
from sqlalchemy.orm import Session
from models.friend import Friends
from schemas.friend import FriendCreate, FriendDelete, FriendUpdateStatus
from crud.friend import create_friend, get_friend_list, update_friend_status, delete_friend
from crud.user import create_user
from schemas.user import UserCreate
from schemas.common import ResponseMessage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# 실제 PostgreSQL DB 사용
test_engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# -----------------------------
# 테스트용 db 세션
# -----------------------------
@pytest.fixture(scope="module")
def db():
    connection = test_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()
    
@pytest.fixture(scope="module")
def user_data(db: Session):
    create_user_data = UserCreate(
        user_id="test_user_123",
        user_pw="hashed_pw", 
        user_nm="테스트유저1",
        user_email="test_user@example.com"
    )
    create_user_data2 = UserCreate(
        user_id="test_user_456",
        user_pw="hashed_pw", 
        user_nm="테스트유저2",
        user_email="test_user2@example.com"
    )

    create_user(create_user_data, db)
    create_user(create_user_data2, db)
    
    yield {
        'user_id': create_user_data.user_id,
        'friend_user_id': create_user_data2.user_id
    }

@pytest.fixture(scope="module")
def friend_data(user_data):
    yield FriendCreate(
        user_id=user_data['user_id'],
        friend_user_id=user_data['friend_user_id'],
        friend_status="PENDING"
    )

def test_create_friend(db: Session, friend_data):
    response = create_friend(friend_data, db)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200

def test_get_friend_list(db: Session, friend_data):
    # 친구 목록 조회
    friends = get_friend_list(friend_data.user_id, db)
    assert isinstance(friends, list)
    assert any(f.user_id == friend_data.user_id for f in friends)

def test_update_friend_status(db: Session, friend_data):
    # 상태 업데이트
    update_data = FriendUpdateStatus(
        user_id=friend_data.user_id,
        friend_user_id=friend_data.friend_user_id,
        friend_status="ACCEPTED"
    )
    response = update_friend_status(update_data, db)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    
def test_delete_friend(db: Session, friend_data):
    # 친구 삭제
    delete_data = FriendDelete(
        user_id=friend_data.user_id,
        friend_user_id=friend_data.friend_user_id
    )
    response = delete_friend(delete_data, db)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200