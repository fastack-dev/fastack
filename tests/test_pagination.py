from fastapi.testclient import TestClient
from requests import Response


def test_pagination(client: TestClient):
    def get_response(page: int = 1, page_size: int = 10) -> Response:
        resp = client.get(
            "/user",
            params={"page": page, "page_size": page_size},
            headers={"Authorization": "Bearer test"},
        )
        return resp

    resp = get_response()
    assert resp.status_code == 200
    assert resp.json()["total"] == 10

    resp = get_response(4)
    assert resp.status_code == 200
    assert resp.json() == {
        "total": 0,
        "paging": {"next": None, "prev": None, "pages": [1, 2]},
        "data": [],
    }
