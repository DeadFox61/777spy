import time
from evo.baccarat import parse_evo
from ezugi.baccarat import parse_ezugi
from loguru import logger
from parse_logger import configure_logger
import threading

configure_logger("baccarat")
evo_thread = threading.Thread(target=parse_evo)
ezugi_thread = threading.Thread(target=parse_ezugi)
evo_thread.start()
ezugi_thread.start()