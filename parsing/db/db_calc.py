import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
from db import _db

def get_conn():
    return _db.get_conn()
def get_cursor(conn):
    return _db.get_cursor(conn)

# Общие
def get_curr_rouls(setting_id):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT r.roul_id
FROM main_roulette r
LEFT JOIN main_usersetting_curr_roulettes sr ON sr.roulette_id = r.id
WHERE usersetting_id = {setting_id}
""")
    roul_ids = []
    rows = cursor.fetchall()
    for row in rows:
        roul_ids.append(row['roul_id'])
    cursor.close()
    conn.close()
    roul_ids.sort()
    return roul_ids

# Статистика
def get_curr(roul_id):
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
    
    
    for row in rows[::-1]:
        nums.append(row['num'])
    cursor.close()
    conn.close()
    return nums

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
def save_stat(roul_id,json_stat):
    stat_str = json.dumps(json_stat)
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
    UPDATE main_roulette
    SET new_stats = '{stat_str}'
    WHERE roul_id = '{roul_id}';
    
""")
    conn.commit()
    cursor.close()
    conn.close()

# Персональная статистика
def ind_save_stat(user_id,json_stat):
    stat_str = json.dumps(json_stat)
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
    UPDATE main_usersetting AS s
    SET individual_stats = '{stat_str}'
    FROM main_user AS u 
    WHERE s.user_id = '{user_id}'
    
""")
    conn.commit()
    cursor.close()
    conn.close()

def get_users_data():
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
        SELECT u.id, s.checked_nums, s.id as setting_id
        FROM main_usersetting AS s
        LEFT JOIN main_user u 
        ON s.user_id = u.id
        WHERE true
    """)
    users_data = {}
    rows = cursor.fetchall()
    for row in rows:
        data = {"checked_nums":row["checked_nums"]}
        rouls_ids = get_curr_rouls(row["setting_id"])
        users_data[row["id"]] = {'data':data,'rouls_ids':rouls_ids}
    cursor.close()
    conn.close()
    return users_data

# Правила

def get_rules():
    rules = []
    conn = get_conn()
    cursor = get_cursor(conn)
    
    cursor.execute(f"""
SELECT r.id as rule_id, r.is_in_row as is_in_order, r.rule_type, r.how_many_in_row as count, r.max_count, u.id as user_id, s.is_zero, s.id as st_id
FROM main_rule r
    LEFT JOIN main_user u 
        ON r.user_id = u.id
    LEFT JOIN main_usersetting s 
        ON s.user_id = u.id
WHERE r.is_tg_on = true
""")
    rules = []
    rows = cursor.fetchall()
    for row in rows:
        row["rouls_ids"] = get_curr_rouls(row["st_id"])
        rules.append(row)
    cursor.close()
    conn.close()

    return rules


def stop_msgs(msgs):
    conn = get_conn()
    cursor = get_cursor(conn)
    for msg in msgs:
        # print(msg)
        cursor.execute(f"""
            UPDATE main_tlgmsg 
            SET is_stoped=True
            WHERE rule_id = '{msg["rule_id"]}' AND user_id = '{msg["user_id"]}' AND roul_name = '{msg["roul_name"]}' AND is_in_order = '{msg["is_in_order"]}' AND rule_name = '{msg["rule_name"]}' AND is_sended = true;
        """)

    conn.commit()
    cursor.close()
    conn.close()

def add_msgs(msgs):
    conn = get_conn()
    cursor = get_cursor(conn)
    for msg in msgs:
        # print(msg)
        cursor.execute(f"""
            INSERT INTO main_tlgmsg (rule_id, user_id, roul_name, is_in_order, rule_name, count, is_sended, is_stoped, msg_id)
            VALUES  ('{msg["rule_id"]}', '{msg["user_id"]}','{msg["roul_name"]}','{msg["is_in_order"]}','{msg["rule_name"]}','{msg["count"]}', false, false, -1);
        """)
    conn.commit()
    cursor.close()
    conn.close()

#ПРАВИЛА БАККАРА

def get_curr_rouls_bacc(setting_id):
    conn = get_conn()
    cursor = get_cursor(conn)
    cursor.execute(f"""
SELECT b.bacc_id
FROM main_usersetting_curr_baccarats c_b
LEFT JOIN main_baccarat b 
        ON b.id = c_b.baccarat_id
WHERE c_b.usersetting_id = {setting_id}
""")
    roul_ids = []
    rows = cursor.fetchall()
    for row in rows:
        roul_ids.append(row['bacc_id'])
    cursor.close()
    conn.close()
    roul_ids.sort()
    return roul_ids


def get_rules_bacc():
    rules = []
    conn = get_conn()
    cursor = get_cursor(conn)
    
    cursor.execute(f"""
SELECT r.id as rule_id, r.rule_type, r.count, u.id as user_id, s.id as st_id
FROM main_baccrule r
    LEFT JOIN main_user u 
        ON r.user_id = u.id
    LEFT JOIN main_usersetting s 
        ON s.user_id = u.id
WHERE r.is_tg_on = true
""")
    rules = []
    rows = cursor.fetchall()
    for row in rows:
        row["baccs_ids"] = get_curr_rouls_bacc(row["st_id"])
        rules.append(row)
    cursor.close()
    conn.close()

    return rules


def stop_msgs_bacc(msgs):
    conn = get_conn()
    cursor = get_cursor(conn)
    for msg in msgs:
        # print(msg)
        cursor.execute(f"""
            UPDATE main_tlgmsgbacc 
            SET is_stoped=True
            WHERE rule_id = '{msg["rule_id"]}' AND user_id = '{msg["user_id"]}' AND bacc_name = '{msg["bacc_name"]}' AND rule_name = '{msg["rule_name"]}' AND is_sended = true;
        """)

    conn.commit()
    cursor.close()
    conn.close()

def add_msgs_bacc(msgs):
    conn = get_conn()
    cursor = get_cursor(conn)
    for msg in msgs:
        # print(msg)
        cursor.execute(f"""
            INSERT INTO main_tlgmsgbacc (rule_id, user_id, bacc_name, rule_name, count, is_sended, is_stoped, msg_id)
            VALUES  ('{msg["rule_id"]}', '{msg["user_id"]}','{msg["bacc_name"]}','{msg["rule_name"]}','{msg["count"]}', false, false, -1);
        """)
    conn.commit()
    cursor.close()
    conn.close()