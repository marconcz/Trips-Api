# Third party imports.
from fastapi.testclient import TestClient

# Local application imports
from src.router.trips import router


client = TestClient(router)


def test_main_route():
    response = client.get("/")
    assert response.json() == {"message": "Hey, It is me fastapi"}
