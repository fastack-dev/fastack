import pytest
from fastapi.testclient import TestClient

from fastack.app import Fastack
from fastack.globals import (
    current_app,
    has_app_context,
    has_request_context,
    has_websocket_context,
    request,
    websocket,
)


@pytest.mark.asyncio
async def test_app_context(app: Fastack):
    with pytest.raises(
        RuntimeError, match="Working outside of application context"
    ) as e:
        current_app.docs_url

    ctx = app.app_context()
    async with ctx:
        assert has_app_context()
        old_token = ctx._token
        ctx.push()
        assert old_token == ctx._token
        assert current_app.docs_url == "/docs"


def test_request_context(app: Fastack, client: TestClient):
    with pytest.raises(RuntimeError, match="Working outside of request context") as e:
        request.query_params

    @app.get("/request_ctx")
    async def req_ctx():
        data = {"success": has_request_context()}
        return data

    resp = client.get("/request_ctx", params={"success": True}).json()
    assert resp["success"] == True


def test_websocket_context(app: Fastack, client: TestClient):
    with pytest.raises(RuntimeError, match="Working outside of websocket context") as e:
        websocket.headers

    @app.websocket("/websocket_ctx")
    async def websocket_ctx():
        await websocket.accept()
        data = {"success": has_websocket_context()}
        await websocket.send_json(data)
        await websocket.close()

    with client.websocket_connect("/websocket_ctx") as ws:
        assert ws.receive_json() == {"success": True}
