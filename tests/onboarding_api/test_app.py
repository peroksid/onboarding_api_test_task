from fastapi.testclient import TestClient
from importlib_resources import files
from onboarding_api.app import app


client = TestClient(app)


def test_get_example_simple_client():
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == files('onboarding_api.example_simple_client').joinpath('index.html').read_text()