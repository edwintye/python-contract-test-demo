import json
from fastapi.testclient import TestClient

from demo.main import app
from demo.items import delete_item

client = TestClient(app)


def test_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"msg": "Healthy"}


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 404


def test_put_item():
    data = {
        "name": "string",
        "description": "another string",
        "price": 5,
        "tax": 100
    }
    response = client.put("/items/1", data=json.dumps(data))
    assert response.status_code == 201


async def delete_item_mock(item_id: int):
    return True


def test_delete_item():
    app.dependency_overrides[delete_item] = delete_item_mock
    with TestClient(app) as mock_client:
        response = mock_client.delete("/items/2")
        assert response.status_code == 200
