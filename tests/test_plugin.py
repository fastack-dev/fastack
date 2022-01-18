from fastapi.testclient import TestClient

from fastack import Fastack
from tests.resources.controllers import PluginYoiController


def test_plugin(
    app: Fastack,
    client: TestClient,
):
    app.include_controller(PluginYoiController())
    resp = client.get("/plugin-yoi", headers={"Authorization": "Bearer test"})
    assert resp.status_code == 200
    assert resp.json() == {"detail": "Yoi", "data": {"msg": "Hello there!"}}
