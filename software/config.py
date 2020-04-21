import json
import pathlib

from log import logger

_config_file_path = pathlib.Path(__file__).parent.absolute() / "config.json"
_config = dict()
try:
    with open(_config_file_path) as json_file:
        _config = json.load(json_file)
except Exception as ex:
    logger.debug("Unable to load json configuration file '{}'".format(_config_file_path))
    logger.debug("Have you copied and renamed config.example.json and updated the settings?")
    logger.debug("Is the json formatted correctly?")
    logger.debug(ex)

def get(key):
    if not key in _config:
        value = input(key + ": ")
        _config[key] = value

    return _config[key]
