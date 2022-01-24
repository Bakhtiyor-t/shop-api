import json
from typing import List, Optional

from fastapi import WebSocket, status, WebSocketDisconnect, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketState

from app.database.database import get_session
from app.database.models import tables
from app.services.auth_service import AuthService


class Connection(BaseModel):
    socket: WebSocket
    tag: Optional[str] = None
    user_id: Optional[int] = None
    company_id: Optional[int] = None
    firm_id: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Connection] = []

    async def connect(self, connection: Connection):
        await connection.socket.accept()
        self.active_connections.append(connection)

    def disconnect(self, connection: Connection):
        self.active_connections.remove(connection)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(
            self,
            message: str,
            tag: str,
            company_id: int,
            firm_id: Optional[int] = None
    ):
        for connection in self.active_connections:
            if connection.firm_id \
                    and connection.firm_id == firm_id:
                await connection.socket.send_text(message)

            elif connection.tag == tag \
                    and connection.company_id == company_id\
                    and not connection.firm_id:
                await connection.socket.send_text(message)

    async def close(self, error: str, connection: Connection):
        message = {
            "detail": "Could not validate credentials",
            "error": error
        }
        json_data = json.dumps(message, ensure_ascii=False)
        await connection.socket.send_text(json_data)
        await connection.socket.close(code=status.WS_1008_POLICY_VIOLATION)
        manager.disconnect(connection)


manager = ConnectionManager()


class WsService:

    def __init__(
            self,
            ws: WebSocket,
            token: Optional[str] = Query(None),
            sesiion: Session = Depends(get_session)
    ):
        self.session = sesiion
        self.ws = ws
        self.token = token

    async def check_token(self):
        try:
            user_id: int = AuthService.verify_token(self.token)
            self.connection.user_id = user_id
            await self.check_permissions(user_id)
        except Exception as e:
            await manager.close(error=e.args, connection=self.connection)

    async def check_permissions(self, user_id: int):
        user: tables.User = self.session.query(tables.User).get(user_id)
        if not user:
            await manager.close(
                error="Такого пользователя нет в базе!",
                connection=self.connection
            )
        elif not user.company_id:
            await manager.close(
                error="Вы не состоите в компании!",
                connection=self.connection
            )
        else:
            self.connection.company_id = user.company_id

    async def get_data(self, tag: str, firm_id: Optional[int] = None):
        self.connection = Connection(
            socket=self.ws,
            tag=tag,
            # this needs to be fixed
            firm_id=firm_id
        )
        await manager.connect(self.connection)
        await self.check_token()
        try:
            if self.ws.application_state == WebSocketState.CONNECTED:
                await self.ws.send_text("Подключение установлено!")
            while True:
                if self.ws.application_state == WebSocketState.DISCONNECTED:
                    break
                print(self.connection.dict())
                await self.ws.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(self.connection)
