from fastapi.testclient import TestClient

from fastack import Fastack
from tests.resources.middleware import AuthMiddleware


def test_middleware(app: Fastack, client: TestClient):
    app.add_middleware(AuthMiddleware)
    response = client.get("/")
    assert response.status_code == 401
    assert response.headers["X-Success"] == "0"
    response = client.get("/", headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.headers["X-Success"] == "1"
