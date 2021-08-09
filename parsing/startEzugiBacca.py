import time
from ezugi.baccarat import parse_ezugi
from parse_logger import get_logger

logger = get_logger()
while True:
    try:
        parse_ezugi()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
