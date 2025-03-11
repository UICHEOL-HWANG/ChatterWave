from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from config.settings import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """JWT 검증 및 디코딩"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")  # 디버깅 로그
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")  # 토큰 만료
        return None
    except jwt.JWTClaimsError:
        print("Invalid claims in the token")  # 잘못된 클레임
        return None
    except JWTError as e:
        print(f"JWT Error: {e}")  # 기타 JWT 에러
        return None