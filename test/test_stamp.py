import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.stamp import Stamps
from crud.user import create_user
from crud.stamp import create_stamp, get_stamp_list
from schemas.stamp import StampCreate
from schemas.common import ResponseMessage
from schemas.user import UserCreate
from core.config import settings

# 실제 PostgreSQL DB 사용
test_engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# -----------------------------
# 테스트용 db 세션
# -----------------------------
@pytest.fixture(scope="function")
def db():
    connection = test_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()
    
# -----------------------------
# 테스트용 사용자 생성
# -----------------------------
@pytest.fixture(scope="function")
def test_user(db):
    user = UserCreate(
        user_id="testuser",
        user_pw="hashed_pw", 
        user_nm="테스트유저",
        user_email="testuser@example.com"
    )
    response = create_user(user, db)
    
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    assert "user created successfully" in response.message
    
    yield user
    # 정리(rollback이 되므로 따로 삭제는 필요 없음)

# -----------------------------
# 스탬프 추가
# -----------------------------
def test_create_stamp(db, test_user):
    # given
    stamp_data = StampCreate(
        user_id=test_user.user_id,
        stamp_nm="테스트스탬프",
        stamp_desc="설명",
        stamp_type="basic",
        total_cnt=10
    )
    # when
    response = create_stamp(stamp_data, db)
    # then
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    assert "stamp created successfully" in response.message
    # 실제 DB에 데이터가 들어갔는지 확인
    stamp = db.query(Stamps).filter(Stamps.user_id == "testuser").first()
    assert stamp is not None
    assert stamp.stamp_nm == "테스트스탬프"


# -----------------------------
# 스탬프 목록 조회(결과없음)
# -----------------------------
def test_get_stamp_list_empty(db, test_user):
    # given
    user_id = test_user.user_id
    # when
    stamps = get_stamp_list(user_id, db)
    # then
    assert isinstance(stamps, list)
    assert len(stamps) == 0


# -----------------------------
# 스탬프 목록 조회(결과있음)
# -----------------------------
def test_get_stamp_list_with_data(db, test_user):
    # given
    user_id = test_user.user_id
    stamp_data = StampCreate(
        user_id=user_id,
        stamp_nm="테스트스탬프",
        stamp_desc="설명",
        stamp_type="basic",
        total_cnt=10
    )
    # when
    response = create_stamp(stamp_data, db)
    assert isinstance(response, ResponseMessage)
    assert response.code == 200
    assert "stamp created successfully" in response.message
    stamps = get_stamp_list(user_id, db)
    # then
    assert isinstance(stamps, list)
    assert len(stamps) != 0

# -----------------------------
# TODO 스탬프 조회
# -----------------------------


# -----------------------------
# TODO 수정
# -----------------------------

    
# -----------------------------
# TODO 진행도 업데이트
# -----------------------------

    
# -----------------------------
# TODO 완료 여부 업데이트
# -----------------------------

    

# -----------------------------
# TODO 삭제
# -----------------------------
