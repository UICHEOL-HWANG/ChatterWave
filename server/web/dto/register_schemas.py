from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True  # Pydantic V2에서는 'from_attributes' 사용