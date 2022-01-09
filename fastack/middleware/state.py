from typing import Union

from starlette.requests import Request
from starlette.websockets import WebSocket

from .base import BaseMiddleware


class StateMiddleware(BaseMiddleware):
    """
    Middleware that combines state in application to request and websocket.
    """

    def update_state(self, object: Union[Request, WebSocket]):
        object.state._state.update(object.app.state._state)

    async def process_request(self, request: Request):
        self.update_state(request)

    async def process_websocket(self, websocket: WebSocket):
        self.update_state(websocket)
