# Third party imports
from fastapi import FastAPI
from uvicorn import Config, Server

# Local application imports
from src.router import trips


def app() -> None:
    app = FastAPI()
    app.include_router(router=trips.router)
    return app


def main() -> None:
    config = Config(app="src.main:app",
                    host="localhost", port=5000,
                    reload=True, factory=True)
    server = Server(config)
    server.run()


if __name__ == "__main__":
    main()
