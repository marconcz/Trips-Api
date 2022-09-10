# Standard library imports
from logging import getLogger

# Local application imports
from src.config import logging
from src.config import server


def main() -> None:
    logging.set_config()
    server.run()


if __name__ == "__main__":
    logger = getLogger("root")
    try:
        main()
    except BaseException as error:
        logger.error(f"Unexpected {error=}, {type(error)=}")
