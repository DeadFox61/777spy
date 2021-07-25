import threading
from ezugi.roulette import parse_ezugi

ez_roul_tr = threading.Thread(target=parse_ezugi)


ez_roul_tr.start()
