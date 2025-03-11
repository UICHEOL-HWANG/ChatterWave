from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    warning_count: int  # 경고 횟수
    is_banned: bool     # 차단 여부

    model_config = {
        "from_attributes": True  # ORM에서 데이터 매핑 가능
    }

