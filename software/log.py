import logging
import logging.handlers

name = 'pager'
logger = logging.getLogger(name)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

fileHandler = logging.handlers.RotatingFileHandler(name + '.log', maxBytes=1048576, backupCount=5)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

# StreamHandler defaults to stderr
consoleHandler = logging.StreamHandler()
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)