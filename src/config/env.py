# Standard library imports
import os

# Third party imports
from dotenv import load_dotenv

load_dotenv()


def set_host(host: str) -> str:
    default_host = "localhost"

    if not host:
        host = default_host
        print("Empty host value, default taken -", default_host)
    return default_host


def set_port(port: str) -> int:
    default_port = 7777

    try:
        default_port = int(port)
    except ValueError as error:
        print(f"{error=}, {type(error)=}")
        print("Invalid port value, default taken -", default_port)
    return default_port


HOST = set_host(os.getenv("HOST"))
PORT = set_port(os.getenv("PORT"))
