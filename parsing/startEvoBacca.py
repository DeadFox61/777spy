import time
from evo.baccarat import parse_evo
from parse_logger import get_logger

logger = get_logger()
while True:
    try:
        parse_evo()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
