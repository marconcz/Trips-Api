# Standard library imports
from yaml import safe_load
from logging.config import dictConfig

def set_config():    
    dict_config = safe_load(open("src/config/logging.yaml", "r"))
    dictConfig(dict_config)
