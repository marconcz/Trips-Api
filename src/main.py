# Standard library imports
from logging import getLogger

# Local application imports
from src.config import server

logger = getLogger(__name__)


def main() -> None:
    server.run()


if __name__ == "__main__":

    try:
        main()
    except BaseException as error:
        logger.error(f"Unexpected {error=}, {type(error)=}")
