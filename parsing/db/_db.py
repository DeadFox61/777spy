import psycopg2
from psycopg2.extras import RealDictCursor
from parse_logger import get_logger
import time

logger = get_logger()

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