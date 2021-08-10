from loguru import logger
from datetime import datetime
import json
from db import _db


@logger.catch
def get_conn():
    return _db.get_conn()
def get_cursor(conn):
    return _db.get_cursor(conn)


def proc_datas(datas):
    conn = get_conn()
    cursor = get_cursor(conn)
    for data in datas:
        try:
            if data['id'] > 0 and 'value' in data and data['value']>= 0 and data['value'] <= 36 and 'action' not in data:
                cursor.execute(f"""
                    INSERT INTO main_number (roulette_id, num, is_new)
                    SELECT  main_roulette.id, '{data['value']}', true
                    FROM    main_roulette
                    WHERE   main_roulette.roul_id = {data['id']};
                    """)
                logger.debug(f"Добавлено в рулетку:{data['id']} значение: {data['value']}")
            elif data['id'] > 0 and 'action' in data and data["action"] == "clear":
                cursor.execute(f"""
                    DELETE 
                    FROM main_number
                    USING main_roulette
                    WHERE main_number.roulette_id = main_roulette.id
                    AND main_roulette.roul_id = {data['id']};""")
                logger.debug(f"Удалили все значения рулетки - {data['id']}")
        except Exception as e:
            logger.error(str(e))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_curr(min_count = 6):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT n.num, r.roul_id 
FROM main_number n
LEFT JOIN main_roulette r ON n.roulette_id = r.id
WHERE n.num >= 0 
ORDER BY n.id DESC LIMIT 500""")
    res = {}
    rows = cursor.fetchall()
    
    
    for row in rows:
        if not row["roul_id"] in res:
            res[row["roul_id"]] = []
        res[row["roul_id"]].append(row['num'])
    for key in res:
        if len(res[key])<min_count:
            res[key]=None
    cursor.close()
    conn.close()
    return res

def get_curr(roul_id, min_count = 6):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT n.num
FROM main_number n
LEFT JOIN main_roulette r ON n.roulette_id = r.id
WHERE n.num >= 0 AND r.roul_id = {roul_id}
ORDER BY n.id DESC LIMIT 50""")
    nums = []
    rows = cursor.fetchall()
    
    
    for row in rows:
        nums.append(row['num'])
    if len(nums)<min_count:
        nums=None
    cursor.close()
    conn.close()
    return nums

def get_evo_id(version = 1000):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT evo_id
FROM main_parsedata
WHERE version = {version}""")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows[0]["evo_id"]

def set_evo_id(evo_id, version = 1000):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"UPDATE main_parsedata SET evo_id='{evo_id}' WHERE version='1000'")
    logger.debug(f"{evo_id} updated")

    conn.commit()
    cursor.close()
    conn.close()


def update_bacca(bacc_id, game_state, stats):
    stats_str = json.dumps(stats)
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
    UPDATE main_baccarat
    SET game_state = '{game_state}', stats = '{stats_str}'
    WHERE bacc_id = '{bacc_id}';

""")
   
    conn.commit()
    cursor.close()
    conn.close()


