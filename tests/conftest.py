from urllib import parse

import pytest
from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient

from . import app as default_app


@pytest.fixture(scope="session")
def app():
    return default_app


@pytest.fixture
def client():
    return TestClient(default_app)


@pytest.fixture
def host():
    return "http://testserver"


@pytest.fixture
def urljoin(host):
    def func(path):
        return parse.urljoin(host, path)

    return func


@pytest.fixture
async def enable_context(app):
    async with LifespanManager(app):
        yield app
