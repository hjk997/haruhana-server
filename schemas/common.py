from pydantic import BaseModel

class ResponseMessage(BaseModel):
    code: int
    message: str
    id: str | None = None
    cnt: int = 0
