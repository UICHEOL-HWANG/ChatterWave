from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 메시지 생성 요청 DTO
class MessageCreate(BaseModel):
    content: str

# 메시지 읽기 응답 DTO
class MessageRead(BaseModel):
    id: int
    content: str
    timestamp: datetime
    username: str

    class Config:
        from_attributes = True  # ORM 모드 활성화

class ChatRoomRead(BaseModel):
    id:int
    name:str
    created_at:datetime
    last_message: Optional[str] = None

    class Config:
        from_attributes = True

class CreateChatRoomPayload(BaseModel):
    room_name: str
    
    