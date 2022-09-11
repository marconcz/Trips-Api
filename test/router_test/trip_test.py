# Third party imports.
from fastapi import FastAPI
from fastapi.testclient import TestClient
# Adds higher directory to python modules path
import sys
sys.path.append("../..") 
# Local application imports
from src.router.trips import router

client = TestClient(router)


def test_main_route():
    response = client.get("/")
    assert response.json() == {"message": "Hey, It is me fastapi"}
