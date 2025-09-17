from datetime import datetime
from pydantic import BaseModel, Field

class StampRecordUpdate(BaseModel):
    stamp_id: str
    step: int
    memo: str | None = None
    is_complete: bool | None = False
    complete_dt: str | None = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    progress_cnt: int 
    is_over_check: bool | None = False
    
