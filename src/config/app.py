# Third party imports
from fastapi import FastAPI

# Local application imports
from src.router import trips


def run():
    app = FastAPI()
    app.include_router(router=trips.router)
    return app
