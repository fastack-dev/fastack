from urllib import parse

import pytest
from fastapi.testclient import TestClient

from fastack import create_app
from tests import settings


@pytest.fixture(scope="session")
def app():
    return create_app(settings)


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def host():
    return "http://testserver"


@pytest.fixture
def urljoin(host):
    def func(path):
        return parse.urljoin(host, path)

    return func
