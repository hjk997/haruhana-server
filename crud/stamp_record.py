from pymongo import MongoClient
from core.config import settings
from schemas.stamp_record import StampRecordUpdate

# MongoDB 연결 (환경에 맞게 수정)
client = MongoClient(settings.MONGO_URL)
db = client["test-database"]  # 사용할 데이터베이스명
collection = db["stamp-info"]  # 사용할 컬렉션명

def init_stamp_record(stamp_id : str, stamp_cnt: int):
    """MongoDB에 데이터 한 건 추가"""
    data = init_data(stamp_id, stamp_cnt)
    result = collection.insert_one(data)
    return result.inserted_id

def find_stamp_record(stamp_id : str):
    """조건에 맞는 첫 번째 문서 조회"""
    query = {"stamp_id": stamp_id}
    return collection.find_one(query)

def find_all_stamp_records():
    """컬렉션의 모든 문서 조회"""
    return list(collection.find({}))

def delete_stamp_record(stamp_id: str):
    """조건에 맞는 문서 한 건 삭제"""
    query = {"stamp_id": stamp_id}
    
    result = collection.delete_one(query)
    return result.deleted_count

def update_stamp_record(stamp_id: str, update_data: StampRecordUpdate):
    """조건에 맞는 문서 한 건 업데이트"""
    result = collection.update_one(
        {"stamp_id": stamp_id},
        {"$set": {
            "data.$[elem].memo": update_data.memo,
            "data.$[elem].is_complete": update_data.is_complete,
            "data.$[elem].complete_dt": update_data.complete_dt
        }},
        array_filters=[{"elem.step": update_data.step}]
    )
    
    return result.modified_count

def init_data(stamp_id : str, stamp_cnt: int):
    """초기 데이터 생성 함수"""
    step_datas = []
    for i in range(1, stamp_cnt + 1):
        step_data = {
            "step": i,
            "memo": None,
            "is_complete": False,
            "complete_dt": None
        }
        step_datas.append(step_data)
    
    return {
        "stamp_id": stamp_id, 
        "total_cnt": stamp_cnt,
        "data": step_datas
    }
    
