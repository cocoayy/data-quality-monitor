from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_alert_detail_not_found() -> None:
    response = client.get("/api/v1/alerts/non-existent-id")
    assert response.status_code in (404, 422)
