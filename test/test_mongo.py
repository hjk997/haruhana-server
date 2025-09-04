import pytest
from service.mongo import (
    init_stamp_record, 
    find_stamp_record, 
    delete_stamp_record,
    find_all_stamp_records,
)

@pytest.fixture(scope="module")
def init_testdata():
    """테스트용 데이터 초기화"""
    yield {
        "stamp_id": "test_stamp_123",
        "stamp_cnt": 50
    }

def test_init_stamp_info(init_testdata):
    # given
    stamp_id = init_testdata["stamp_id"]
    stamp_cnt = init_testdata["stamp_cnt"]
    # when
    inserted_id = init_stamp_record(stamp_id, stamp_cnt)
    # then
    assert inserted_id is not None

def test_find_stamp_info(init_testdata):
    # given
    stamp_id = init_testdata["stamp_id"]
    # when
    stamp = find_stamp_record(stamp_id)
    # then
    assert stamp is not None
    assert stamp["stamp_id"] == stamp_id
    print(stamp)

def test_find_all_stamp_info(init_testdata):
    # given
    # when
    stamps = find_all_stamp_records()
    # then
    assert len(stamps) > 0
    assert stamps[0]["stamp_id"] == init_testdata["stamp_id"]

def test_delete_stamp_info(init_testdata):
    # given
    stamp_id = init_testdata["stamp_id"]
    # when
    deleted_count = delete_stamp_record(stamp_id)
    # then
    assert deleted_count == 1
