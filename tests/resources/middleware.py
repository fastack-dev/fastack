from fastapi import HTTPException, Request, Response, WebSocket, status

from fastack.middleware.base import BaseMiddleware


class AuthMiddleware(BaseMiddleware):
    async def process_request(self, request: Request):
        await process_request(request)

    async def process_response(self, response: Response, exc: Exception = None):
        await process_response(response, exc)

    async def process_websocket(self, websocket: WebSocket):
        await process_websocket(websocket)


async def process_request(request: Request):
    auth = request.headers.get("Authorization")
    if auth != "Bearer test":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


async def process_response(response: Response, exc: Exception = None):
    response.headers["X-Success"] = "1" if response.status_code == 404 else "0"


async def process_websocket(websocket: WebSocket):
    # accept all incoming connections
    await websocket.accept()
