# Third party imports
from uvicorn import Config, Server

# Local application imports
from src.config import env


def run():
    config = Config(app="src.config.app:run",
                    host=env.HOST, port=env.PORT,
                    reload=True, factory=True)
    server = Server(config)
    server.run()
