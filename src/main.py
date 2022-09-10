# Third party imports
from fastapi import FastAPI

# Local application imports
from src import trips

app = FastAPI()
app.include_router(trips.router)

#from uvicorn import Config, Server
"""
def main():
    app = FastAPI()
    app.include_router(trips.router)

    config = Config("main:app", port=5000)
    server = Server(config)
    server.run()

main()
"""