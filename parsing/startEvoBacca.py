import time
from evo.baccarat import parse_evo
from loguru import logger
from parse_logger import configure_logger

configure_logger("evo_bacc")
while True:
    try:
        parse_evo()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
