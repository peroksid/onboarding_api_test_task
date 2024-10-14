from fastapi.testclient import TestClient
from importlib_resources import files
from onboarding_api.app import app
from onboarding_api.db import get_pool
from onboarding_api.storage import save_file
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


def test_upload_chunk():
    expected_chunk_id = 424242
    def get_pool_override():
        mock = MagicMock()
        mock.connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value.__getitem__.side_effect = [
            1,                  # upload exists
            2,                  # chunk does not exist
            expected_chunk_id   # chunk db id
        ]
        return mock

    def save_file_override():
        return lambda upload_id, chunk_number, content_bytes: f'/tmp/mock_storage/{upload_id}/{chunk_number}'
    
    app.dependency_overrides[get_pool] = get_pool_override
    app.dependency_overrides[save_file] = save_file_override

    import base64
    import hashlib
    session_token = hashlib.sha256().hexdigest()
    content = ''.join(["x" for _ in range(4000)])
    content_bytes = content.encode()
    content_size = len(content)
    content_hash = hashlib.sha256(content_bytes).hexdigest()
    content_b64 = base64.b64encode(content_bytes).decode()
    data = {
        'number': 1,
        'size': content_size,
        'hash': content_hash,
        'b64_bytes': content_b64
    }
    response = client.post("/upload/424242/chunk", headers={'x-session-token': session_token}, json=data)
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200, response.text
    assert data["chunk_id"] == expected_chunk_id
