from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from config.models import Member

from .hasing import hash_password  # 모듈화된 해싱 함수 가져오기

from dto.register_schemas import RegisterUser

register_router = APIRouter(
    prefix="/user",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@register_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    """회원가입"""
    # 기존 사용자 체크
    existing_user = db.query(Member).filter(
        (Member.username == user.username) | (Member.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    # 새 사용자 생성
    new_user = Member(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username}
