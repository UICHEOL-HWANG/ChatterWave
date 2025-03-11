# utils/connection_manager.py
from typing import Dict, List
from fastapi import WebSocket

class ConnectManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}  # room_id를 키로 사용

    async def connect(self, websocket: WebSocket, room_id: int):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: int):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)
