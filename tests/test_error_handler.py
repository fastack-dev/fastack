import pytest
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from fastack import Fastack


def test_http_exception(app: Fastack, client: TestClient):
    @app.middleware.process_request
    async def raise_error(request: Request):
        if "X-Test-Error" in request.headers:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "test error")

    resp = client.get("/", headers={"X-Test-Error": "1"})
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "test error"}


def test_custom_error_handler(app: Fastack, client: TestClient):
    class OurException(Exception):
        def __init__(self, message: str):
            self.message = message

    def sync_handler(request: Request, exc: OurException):
        return JSONResponse(
            {"error": True, "message": exc.message},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    app.add_exception_handler(OurException, sync_handler)

    @app.middleware.process_request
    async def raise_error(request: Request):
        if "X-Custom-Error" in request.headers:
            raise OurException("Custom error")

    resp = client.get("/", headers={"X-Custom-Error": "1"})
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert resp.json() == {"error": True, "message": "Custom error"}


def test_unknown_error_handler(app: Fastack, client: TestClient):
    class UnknownException(Exception):
        pass

    @app.middleware.process_request
    async def raise_error(request: Request):
        if "X-Unknown-Error" in request.headers:
            raise UnknownException("Unknown error")

    with pytest.raises(UnknownException, match="Unknown error"):
        client.get("/", headers={"X-Unknown-Error": "1"})
