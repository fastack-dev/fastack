from typing import Union

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket

from .globals import request, websocket


class BaseMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope_type = scope["type"]
        if scope_type == "http":
            await self.process_request(request)
        elif scope_type == "websocket":
            await self.process_websocket(websocket)

        return await super().__call__(scope, receive, send)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        await self.process_response(response)
        return response

    async def process_request(self, request: Request):
        raise NotImplementedError

    async def process_response(self, response: Response):
        pass

    async def process_websocket(self, websocket: WebSocket):
        raise NotImplementedError


class MergeAppStateMiddleware(BaseMiddleware):
    def update_state(self, object: Union[Request, WebSocket]):
        object.state._state.update(object.app.state._state)

    async def process_request(self, request: Request):
        self.update_state(request)

    async def process_websocket(self, websocket: WebSocket):
        self.update_state(websocket)
