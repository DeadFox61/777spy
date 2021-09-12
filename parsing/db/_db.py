import psycopg2
from psycopg2.extras import RealDictCursor
from loguru import logger
import time
import os

def get_conn(host = 'postgresdb'):
    while True:
        try:
            return psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
                               password=os.environ.get('POSTGRES_PASSWORD'), host=host)
        except Exception as e:
            logger.error(f"{str(e)} can't connect to db, retry in 5 sec")
            time.sleep(5)
def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)