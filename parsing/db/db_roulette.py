from loguru import logger
from datetime import datetime
import json
from db import _db

def get_conn():
    return _db.get_conn()
def get_cursor(conn):
    return _db.get_cursor(conn)


def clear_roul(roul_id):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
        DELETE 
        FROM main_number
        USING main_roulette
        WHERE main_number.roulette_id = main_roulette.id
        AND main_roulette.roul_id = {roul_id};""")
    conn.commit()
    cursor.close()
    conn.close()

def add_numbers(roul_id, nums):
    conn = get_conn()
    cursor = get_cursor(conn)
    for num in nums[::-1]:
        cursor.execute(f"""
            INSERT INTO main_number (roulette_id, num)
            SELECT  main_roulette.id, '{num}'
            FROM    main_roulette
            WHERE   main_roulette.roul_id = {roul_id};
        """)
    conn.commit()
    cursor.close()
    conn.close()

def get_roul_data():
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT id, roul_id, name
FROM main_roulette""")
    roul_data = []
    rows = cursor.fetchall()
    
    
    for row in rows:
        roul_data.append({"id":row["id"],"roul_id":row['roul_id'],"name":row["name"]})
    cursor.close()
    conn.close()
    return roul_data

def get_curr_nums(roul_id):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT n.num
FROM main_number n
LEFT JOIN main_roulette r ON n.roulette_id = r.id
WHERE n.num >= 0 AND r.roul_id = {roul_id}
ORDER BY n.id DESC LIMIT 500""")
    nums = []
    rows = cursor.fetchall()
    
    for row in rows:
        nums.append(row['num'])
    cursor.close()
    conn.close()
    return nums


def get_init_data():
    data = {}
    rouls = get_roul_data()
    
    for roul in rouls:
        data[roul["roul_id"]] = {'name': roul['name'], 'nums' : get_curr_nums(roul["roul_id"])}
    return data