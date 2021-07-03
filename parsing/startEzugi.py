import time
from ezugi.roulette import parse_ezugi

while True:
    try:
        parse_ezugi()
    except Exception as e:
        print(e)
        time.sleep(10)
