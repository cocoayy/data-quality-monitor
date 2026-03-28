from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_datasets_invalid_sort_by() -> None:
    response = client.get("/api/v1/datasets?sort_by=invalid_field")
    assert response.status_code == 422


def test_datasets_invalid_sort_order() -> None:
    response = client.get("/api/v1/datasets?sort_order=sideways")
    assert response.status_code == 422
