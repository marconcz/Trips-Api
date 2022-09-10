# Standard library imports
import logging
from yaml import safe_load
from logging.config import dictConfig

def set_config():
    FPATH = "src/config/logging.yaml"
    FMODE = "r"

    try:
        with open(FPATH, FMODE) as file:
            dict_config = safe_load(file)
            dictConfig(dict_config)
    except OSError as error:
        logging.error(f"{error=}, {type(error)=}")
