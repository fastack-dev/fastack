from typing import Callable

import pytest
from fastapi.testclient import TestClient

from fastack import Controller, Fastack
from tests.resources.controllers import CustomController, UserController


@pytest.mark.parametrize(
    ["controller", "url_prefix", "get_endpoint"],
    [
        (UserController, "/user", "/{id}"),
        (CustomController, "/custom", "/get/{id}"),
    ],
)
def test_controller(
    app: Fastack,
    client: TestClient,
    urljoin: Callable,
    controller: Controller,
    url_prefix: str,
    get_endpoint: str,
):
    app.include_controller(controller())
    uid = 1
    path = (url_prefix + get_endpoint).format(id=uid)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {
        "detail": "User",
        "data": {"id": uid, "url": urljoin(path)},
    }

    response = client.post(url_prefix, json={"name": "John Doe"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Created", "data": {"name": "John Doe"}}

    path = url_prefix + "/" + str(uid)
    response = client.put(path, json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Updated",
        "data": {"id": uid, "name": "Jane Doe"},
    }

    response = client.delete(path)
    assert response.status_code == 200
    assert response.json() == {"detail": "Deleted", "data": {"id": uid}}
