# Third party imports
from fastapi import FastAPI
from uvicorn import Config, Server

# Local application imports
from src.router import trips
from src.config import env


def app() -> None:
    app = FastAPI()
    app.include_router(router=trips.router)
    return app


def main() -> None:
    config = Config(app="src.main:app",
                    host=env.HOST, port=env.PORT,
                    reload=True, factory=True)
    server = Server(config)
    server.run()


if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        print(f"Unexpected {error=}, {type(error)=}")
