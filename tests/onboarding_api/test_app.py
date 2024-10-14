from fastapi.testclient import TestClient
from importlib_resources import files
from onboarding_api.app import app
from onboarding_api.db import get_pool
from uuid import UUID, uuid4

client = TestClient(app)


def test_get_example_simple_client():
    response = client.get("/")
    assert response.status_code == 200
    assert (
        response.text
        == files("onboarding_api.example_simple_client")
        .joinpath("index.html")
        .read_text()
    )


from unittest.mock import MagicMock


def test_initiate_upload():
    def get_pool_override():
        mock = MagicMock()
        mock.connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value.__getitem__.return_value = (
            424242
        )
        return mock

    app.dependency_overrides[get_pool] = get_pool_override
    sentinel_uuid = UUID("{12345678-1234-5678-1234-567812345678}")
    app.dependency_overrides[uuid4] = lambda: sentinel_uuid

    hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    response = client.post(
        "/upload",
        json={
            "file_info": {
                "name": "the name",
                "size": 4242,
                "mime": "text/plain",
                "hash": hash,
            }
        },
    )
    app.dependency_overrides.clear()

    data = response.json()
    assert response.status_code == 200
    assert data["upload_id"] == 424242
    assert data["session_token"] == str(sentinel_uuid)
