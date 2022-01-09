from fastapi import Request, Response, WebSocket
from fastapi.testclient import TestClient

from fastack import Fastack
from fastack.globals import websocket
from tests.resources.middleware import (  # noqa
    AuthMiddleware,
    process_request,
    process_response,
    process_websocket,
)


def test_middleware(app: Fastack, client: TestClient):
    # app.add_middleware(AuthMiddleware)

    @app.middleware("request")
    async def on_request(request: Request):
        await process_request(request)

    @app.middleware("response")
    async def on_response(response: Response, exc: Exception = None):
        await process_response(response, exc)

    @app.middleware("websocket")
    async def on_websocket(ws: WebSocket):
        await process_websocket(ws)

    response = client.get("/")
    assert response.status_code == 401
    assert response.headers["X-Success"] == "0"
    response = client.get("/", headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.headers["X-Success"] == "1"

    @app.websocket("/ws")
    async def hello_ws():
        await websocket.send_json({"hello": "world"})
        await websocket.close()

    with client.websocket_connect("/ws") as ws:
        assert ws.receive_json() == {"hello": "world"}
