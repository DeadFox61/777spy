import time
from ezugi.roulette import parse_ezugi
from loguru import logger
from parse_logger import configure_logger

configure_logger("ezugi_roul")
while True:
    try:
        parse_ezugi()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
