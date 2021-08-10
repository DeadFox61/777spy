import time
from evo.evo_id import parse_evo_id
from loguru import logger
from parse_logger import configure_logger

configure_logger("id")
while True:
    try:
        parse_evo_id()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
