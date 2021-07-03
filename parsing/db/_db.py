import psycopg2
from psycopg2.extras import RealDictCursor
from loguru import logger
import time

logger.add("logs/parse.log", format="{time} {level} {message}", rotation="100 MB", compression = "zip") 

def get_conn():
    while True:
        try:
            return psycopg2.connect(dbname='roulette', user='roul',
                               password='As3Vdsd898', host='postgresdb')
        except Exception as e:
            logger.error(f"{str(e)} can't connect to db, retry in 5 sec")
            time.sleep(5)
def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)