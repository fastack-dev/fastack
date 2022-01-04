import pytest
from fastapi.testclient import TestClient

from .app.main import app as fastapi_app


@pytest.fixture()
def client():
    return TestClient(fastapi_app)
