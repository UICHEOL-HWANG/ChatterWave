from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from dto.chat_schemas import MessageCreate, MessageRead, ChatRoomRead, CreateChatRoomPayload


from utils.connection_manager import ConnectManager
from cached.redis_manager import RedisManager

from datetime import datetime

from config.database import get_db
from config.models import Message, Member, ChatRoom, HateSpeechLog, chat_room_members 

from security.auth import *

from security.jwt import decode_access_token

from .classify_text import classify_text

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)

manager = ConnectManager()
redis = RedisManager()


# 채팅방 생성


@chat_router.post("/rooms")
def create_chat_room(
    payload: CreateChatRoomPayload,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    # 중복 이름 확인
    existing_room = db.query(ChatRoom).filter(ChatRoom.name == payload.room_name).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Chat room name already exists")

    # 채팅방 생성
    chat_room = ChatRoom(
        name=payload.room_name,
        created_by=current_user.id
    )
    db.add(chat_room)
    db.commit()
    db.refresh(chat_room)

    # 현재 사용자를 채팅방 멤버로 추가
    chat_room.members.append(current_user)
    db.commit()

    return {
        "id": chat_room.id,
        "name": chat_room.name,
        "created_at": chat_room.created_at,
    }

@chat_router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, token: str, db: Session = Depends(get_db)):
    try:
        await websocket.accept()

        # JWT 토큰 검증
        payload = decode_access_token(token)
        if not payload:
            await websocket.send_json({"error": "Invalid token"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        username = payload.get("sub")
        user = db.query(Member).filter(Member.username == username).first()
        if not user:
            await websocket.send_json({"error": "User not found"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Redis에서 차단 상태 확인
        is_banned = redis.check_ban_status(user.id)
        if is_banned:
            await websocket.send_json({"error": "User is banned"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # 채팅방 존재 여부 확인
        chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not chat_room:
            await websocket.send_json({"error": "Chat room not found"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # WebSocket 매니저에 사용자 등록
        await manager.connect(websocket, room_id)
        print(f"User {username} connected to room {room_id}")

        while True:
            try:
                # 메시지 수신
                data = await websocket.receive_json()
                content = data.get("message")
                if not content:
                    await websocket.send_json({"error": "Empty message"})
                    continue

                # 혐오 표현 필터링
                classify_result = await classify_text([content])
                label = classify_result[0]["label"]

                if label == "혐오":
                    is_banned = redis.increment_hate_count(user.id, db)
                    warning_count = redis.get_hate_count(user.id)

                    # 🚨 혐오 표현 로그 DB 저장
                    hate_speech_log = HateSpeechLog(
                        user_id=user.id,
                        chat_room_id=room_id,
                        content=content,
                        warning_count=warning_count,
                        username=user.username
                    )
    
                    
                    
                    db.add(hate_speech_log)
                    
                    

                    # 사용자 경고 횟수 증가 (Member 테이블의 warnings 필드 업데이트)
                    user.warnings = warning_count  # Member 모델의 warnings 필드 업
                    db.commit()

                    if is_banned:
                        # 🚨 해당 사용자에게 차단 알림 (alert)
                        await websocket.send_json({
                            "username": "System",
                            "content": "차단되었습니다. 더 이상 메시지를 보낼 수 없습니다.",
                            "alert": True,  # 클라이언트에서 alert 처리
                            "redirect": True
                        })

                        # ⚠️ 방 전체에 차단 알림 브로드캐스트
                        await manager.broadcast(
                            {"username": "System", "content": f"{username}님이 차단되었습니다.", "room_id": room_id},
                            room_id
                        )

                        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                        return

                    # 🚨 사용자에게 개별적으로 경고 알림
                    await websocket.send_json({
                        "username": "System",
                        "content": f"경고 {warning_count}/3: 혐오 표현이 감지되었습니다.",
                        "alert": True  # 클라이언트에서 alert 처리
                    })

                    # ⚠️ 방 전체에 시스템 메시지로 경고 알림
                    await manager.broadcast(
                        {"username": "System", "content": f"{username}님이 경고 {warning_count}/3을 받았습니다.", "room_id": room_id},
                        room_id
                    )
                    continue

                # 메시지 저장 및 브로드캐스트
                message = Message(content=content, user_id=user.id, chat_room_id=room_id)
                db.add(message)
                db.commit()

                # 현재 시간을 ISO 형식으로 추가
                timestamp = datetime.utcnow().isoformat()

                # 브로드캐스트 메시지에 시간 추가
                await manager.broadcast(
                    {
                        "username": username,
                        "content": content,
                        "room_id": room_id,
                        "timestamp": timestamp  # 시간 추가
                    },
                    room_id
                )

            except WebSocketDisconnect:
                print(f"User {username} disconnected from room {room_id}")
                manager.disconnect(websocket, room_id)
                break

            except Exception as e:
                print(f"Message handling error: {e}")
                await websocket.send_json({"error": "Internal server error"})
                break

    except Exception as e:
        print(f"Critical WebSocket Error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)



# 채팅방 멤버 초대
@chat_router.post("/rooms/{room_id}/invite")
def invite_member_to_chat_room(room_id: int, member_id: int, db: Session = Depends(get_db)):
    """
    채팅방에 멤버 초대
    """
    chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member in chat_room.members:
        raise HTTPException(status_code=400, detail="Member is already in the chat room")

    chat_room.members.append(member)
    db.commit()
    return {"message": f"Member {member.username} added to chat room {chat_room.name}"}

# 채팅방 나가기
@chat_router.post("/rooms/{room_id}/leave")
def leave_chat_room(room_id: int, member_id: int, db: Session = Depends(get_db)):
    """
    채팅방 나가기
    """
    chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member not in chat_room.members:
        raise HTTPException(status_code=400, detail="Member is not part of the chat room")

    chat_room.members.remove(member)
    db.commit()
    return {"message": f"Member {member.username} has left the chat room {chat_room.name}"}


# 채팅방 조회
@chat_router.get("/rooms", response_model=list[ChatRoomRead])
def get_chat_rooms(db: Session = Depends(get_db), current_user: Member = Depends(get_current_user)):
    """
    사용자가 속한 채팅방 목록을 조회
    """
    # 사용자가 속한 채팅방만 조회
    chat_rooms = db.query(ChatRoom).join(chat_room_members).filter(chat_room_members.c.member_id == current_user.id).all()

    response = []
    for room in chat_rooms:
        # 마지막 메시지 조회
        last_message = (
            db.query(Message.content)
            .filter(Message.chat_room_id == room.id)
            .order_by(Message.timestamp.desc())
            .first()
        )

        response.append(
            ChatRoomRead(
                id=room.id,
                name=room.name,
                created_at=room.created_at,
                last_message=last_message[0] if last_message else None
            )
        )

    return response




# 특정 채팅방에 입장하기 위한 로직 
@chat_router.post("/rooms/{room_id}/join")
def join_chat_room(room_id: int, db: Session = Depends(get_db), current_user: Member = Depends(get_current_user)):
    """
    사용자가 특정 채팅방에 입장
    """
    chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    if current_user in chat_room.members:
        return {"message": f"You are already in the chat room {chat_room.name}"}

    chat_room.members.append(current_user)
    db.commit()

    return {"message": f"User {current_user.username} joined chat room {chat_room.name}"}









@chat_router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int, db: Session = Depends(get_db), current_user: Member = Depends(get_current_user)):
    """
    채팅방 메시지 조회
    """
    chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    if current_user not in chat_room.members:
        raise HTTPException(status_code=403, detail="User is not a member of this chat room")

    messages = (
        db.query(Message)
        .filter(Message.chat_room_id == room_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    # 디버깅 로그
    print(f"🔍 쿼리된 메시지: {[message.content for message in messages]}")

    return [
        {
            "id": message.id,
            "username": db.query(Member.username).filter(Member.id == message.user_id).scalar(),
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        }
        for message in messages
    ]
