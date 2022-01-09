from fastapi import HTTPException, Request, Response, WebSocket, status


def is_approved(request: Request) -> bool:
    auth = request.headers.get("Authorization")
    if auth != "Bearer test":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


async def process_request(request: Request):
    is_approved(request)


async def process_response(response: Response, exc: Exception = None):
    response.headers["X-Success"] = "1" if response.status_code == 404 else "0"


async def process_websocket(websocket: WebSocket):
    # accept all incoming connections
    await websocket.accept()
