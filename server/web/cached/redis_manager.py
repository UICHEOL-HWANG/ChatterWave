import redis
import threading
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from config.models import Member  # Member 모델 import

class RedisManager:

    def __init__(self, host: str = "redis-server", port: int = 6379, password: str = None):
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

    def cache_message(self, room_id: int, message: str, max_messages: int = 50):
        """특정 채팅방의 메시지 캐싱"""
        key = f"chatroom:{room_id}"
        self.client.lpush(key, message)
        self.client.ltrim(key, 0, max_messages - 1)

    def get_cached_messages(self, room_id: int):
        """특정 채팅방의 캐싱된 메시지 조회"""
        key = f"chatroom:{room_id}"
        return self.client.lrange(key, 0, -1)

    def increment_hate_count(self, user_id: int, db: Session, max_limit: int = 3) -> bool:
        """
        유저의 혐오 표현 경고 횟수 증가 및 차단 여부 확인 (50초 후 자동 해제 포함)
        """
        key = f"user:{user_id}:hate_count"
        count = self.client.incr(key)  # 🚀 혐오 표현 감지 횟수 증가

        if count == 1:
            self.client.expire(key, 50)  # ⏳ 50초 후 초기화 (경고 횟수 리셋)

        # 🚨 3회 이상 혐오 표현 감지되면 차단
        if count >= max_limit:
            self.update_ban_status(user_id, True, db)
            
            # 💡 50초 후 차단 해제 & 혐오 표현 횟수 초기화
            threading.Timer(50, self.unban_user, args=(user_id, db)).start()
            return True  # 차단됨

        return False  # 아직 차단되지 않음
    
    def get_hate_count(self, user_id: int) -> int:
        """유저의 혐오 표현 감지 횟수 반환"""
        key = f"user:{user_id}:hate_count"
        count = self.client.get(key)
        return int(count) if count else 0  # 값이 없으면 0 반환


    def unban_user(self, user_id: int, db: Session):
        """
        50초 후 자동으로 차단 해제
        """
        self.update_ban_status(user_id, False, db)  # 차단 해제
        self.reset_hate_count(user_id)  # 🚀 혐오 표현 감지 횟수 초기화
        print(f"✅ User {user_id} has been unbanned after 50 seconds.")

    def reset_hate_count(self, user_id: int):
        """유저의 혐오 표현 경고 횟수 초기화"""
        key = f"user:{user_id}:hate_count"
        self.client.delete(key)

    def check_ban_status(self, user_id: int) -> bool:
        """유저 차단 상태 확인"""
        key = f"user:{user_id}:is_banned"
        status = self.client.get(key)
        return status == "1"

    def update_ban_status(self, user_id: int, is_banned: bool, db: Session):
        """
        유저 차단 상태를 Redis 및 DB에 반영
        """
        key = f"user:{user_id}:is_banned"
    
        if is_banned:
            self.client.setex(key, 50, "1")  # ⏳ 50초 후 자동 해제
        else:
            self.client.delete(key)  # 🚀 차단 해제 시 삭제

        # DB 업데이트
        user = db.query(Member).filter(Member.id == user_id).first()
        if user:
            user.is_blocked = is_banned
            db.commit()
