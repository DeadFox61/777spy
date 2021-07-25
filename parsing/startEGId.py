import time
from evo.evo_id import parse_evo_id
from parse_logger import get_logger

logger = get_logger()
while True:
    try:
        parse_evo_id()
    except Exception as e:
        logger.error(e)
        time.sleep(10)
