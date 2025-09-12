import pytest
from sqlalchemy.orm import Session
from crud.user import create_user
from models.notice import Notices
from schemas.notice import NoticeCreate, NoticeDelete, NoticeList, NoticeUpdateRead, NoticeUpdateSend
from crud.notice import create_notice, get_notice_list,  delete_notice, read_notice, send_notice
from schemas.common import ResponseMessage
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from uuid import uuid4

from schemas.user import UserCreate

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
    
    create_user(create_user_data, db)
    
    yield {
        'user_id': create_user_data.user_id,
    }
    
@pytest.fixture(scope="module")
def test_notice_data(user_data):
    yield NoticeCreate(
        user_id=user_data['user_id'],
        notice_type="INFO",
        notice_message="테스트 알림입니다.",
        is_read=False,
        is_send=False,
        is_delete=False,
        create_dt=date.today() 
    )

def test_create_notice(db: Session, test_notice_data):
    response = create_notice(test_notice_data, db)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200

@pytest.fixture(scope="module")
def create_notice_fixture(db: Session, test_notice_data):
    response = create_notice(test_notice_data, db)
    yield response

def test_send_notice(db: Session, test_notice_data, create_notice_fixture):
    # given
    notice_update = NoticeUpdateSend(
        user_id=test_notice_data.user_id
    )
    # when 
    response = send_notice(notice_update, db)
    # then 
    assert isinstance(response, ResponseMessage)
    assert response.code == 200

def test_get_notice_list(db: Session, test_notice_data, create_notice_fixture):
    # given
    notice_list = NoticeList(
        user_id=test_notice_data.user_id,
        skip=0,
        limit=10
    )
    # when
    notices = get_notice_list(notice_list, db)
    # then
    assert isinstance(notices, list)
    assert any(str(n.notice_id) == create_notice_fixture.id for n in notices)

def test_read_notice(db: Session, create_notice_fixture):
    # given
    notice_update = NoticeUpdateRead(
        notice_id=create_notice_fixture.id
    )
    # when 
    response = read_notice(notice_update, db)
    # then
    assert isinstance(response, ResponseMessage)
    assert response.code == 200

def test_delete_notice(db: Session, create_notice_fixture):
    # given
    notice_delete = NoticeDelete(
        notice_id=create_notice_fixture.id
    )
    # when
    response = delete_notice(notice_delete, db)
    # then
    assert isinstance(response, ResponseMessage)
    assert response.code == 200