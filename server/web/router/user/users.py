from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from dto.token_schemas import Token
from dto.user_schemas import UserRead

from datetime import timedelta

from security.auth import authenticate_user
from security.jwt import create_access_token
from security.auth import get_current_user

from config.settings import settings
from config.database import get_db
from config.models import Member

from cached.redis_manager import RedisManager


# Cached

redis_manager = RedisManager()

auth_router = APIRouter(
    prefix="/user",
    tags=["Authentication & User Service"],
    responses={404: {"description": "Not found"}},
)

#회원정보 조회

# 회원정보 조회
@auth_router.get("/all_users", response_model=list[UserRead])
async def get_all_users(db: Session = Depends(get_db)):
    """
    모든 사용자 정보 반환
    """
    users = db.query(Member).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    user_data = []
    for user in users:
        # Redis에서 경고 횟수 및 차단 상태 조회
        warning_count = redis_manager.get_hate_count(user.id)
        is_banned = redis_manager.check_ban_status(user.id)

        # Redis에 데이터가 없으면 DB에서 가져와 Redis에 동기화
        if warning_count == 0:
            warning_count = user.warnings  or 0
            redis_manager.client.set(f"user:{user.id}:hate_count", warning_count)

        if not is_banned:
            is_banned = user.is_blocked or False
            redis_manager.client.set(f"user:{user.id}:is_banned", "1" if is_banned else "0")

        user_data.append(
            UserRead(
                id=user.id,
                username=user.username,
                email=user.email,
                warning_count=warning_count,
                is_banned=is_banned
            )
        )

    return user_data


# 로그인

@auth_router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    사용자 로그인 및 JWT 토큰 발급
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 차단 여부 확인
    is_banned = redis_manager.check_ban_status(user.id)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_banned": is_banned  # 차단 여부 추가
    }

# 회원 조회

@auth_router.get("/my_account", response_model=UserRead)
def read_users_me(current_user: Member = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    현재 로그인한 사용자 정보 반환
    """
    # Redis에서 경고 횟수 및 차단 상태 조회
    warning_count = redis_manager.get_hate_count(current_user.id)
    is_banned = redis_manager.check_ban_status(current_user.id)

    # Redis에 데이터가 없으면 DB에서 가져와 Redis에 동기화
    if warning_count == 0:
        warning_count = current_user.warnings  or 0
        redis_manager.client.set(f"user:{current_user.id}:hate_count", warning_count)

    if not is_banned:
        is_banned = current_user.is_blocked or False
        redis_manager.client.set(f"user:{current_user.id}:is_banned", "1" if is_banned else "0")

    return UserRead(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        warning_count=warning_count,
        is_banned=is_banned
    )


