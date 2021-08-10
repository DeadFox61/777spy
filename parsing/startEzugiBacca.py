import time
from ezugi.baccarat import parse_ezugi
from loguru import logger
from parse_logger import configure_logger

configure_logger("ezugi_bacc")
while True:
    try:
        parse_ezugi()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
