from http import HTTPStatus

from fastapi.testclient import TestClient
from studyhive.main import app


def test_liveness_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "service": "studyhive-api",
        "status": "ok",
        "version": "0.0.0",
    }
