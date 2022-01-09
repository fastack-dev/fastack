from fastapi.testclient import TestClient

from fastack import Fastack
from fastack.globals import websocket
from tests.resources.middleware import (
    process_request,
    process_response,
    process_websocket,
)


def test_middleware(app: Fastack, client: TestClient):
    app.middleware("request")(process_request)
    app.middleware("response")(process_response)
    app.middleware("websocket")(process_websocket)
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
