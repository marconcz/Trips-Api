# Third party imports
from uvicorn import Config, Server

# Local application imports
from src.config import env


def run(PORT):
    config = Config(
        app="src.config.app:run",
        host=env.HOST,
        port=PORT,
        reload=True,
        factory=True,
    )
    server = Server(config)
    server.run()
