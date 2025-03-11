from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    is_banned : bool

class TokenData(BaseModel):
    username: Optional[str] = None