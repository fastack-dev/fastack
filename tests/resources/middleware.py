from typing import Union

from fastapi import HTTPException, Request, Response, WebSocket, status

from fastack.middleware import BaseMiddleware


class AuthMiddleware(BaseMiddleware):
    def is_approved(self, obj: Union[Request, WebSocket]) -> bool:
        auth = obj.headers.get("Authorization")
        if not auth:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

        if auth != "Bearer test":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

    async def process_request(self, request: Request):
        self.is_approved(request)

    async def process_response(self, response: Response, exc: Exception = None):
        response.headers["X-Success"] = "1" if exc is None else "0"

    async def process_websocket(self, websocket: WebSocket):
        self.is_approved(websocket)
