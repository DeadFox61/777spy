import websocket
import json
import time
from loguru import logger

from db import db_main as db
from utils.rules_bacc import Rules

BACCARAT_NAMES = {
    "100": "Baccarat",
    "101": "Speed Cricket Baccarat",
    "26100": "Baccarat Pro 1",
    "26101": "Baccarat Pro 2",
    "41100": "Salsa Baccarat 1",
    "41101": "Salsa Baccarat 2",
    "32100": "Casino Marina Baccarat 1",
    "32101": "Casino Marina Baccarat 2",
    "32102": "Casino Marina Baccarat 3",
    "32103": "Casino Marina Baccarat 4",
    "120": "Baccarat Knock Out",
    "130": "Baccarat Super 6",
    "150": "Dragon Tiger",
    "170": "Baccarat No Commission",
    "43100": "Fiesta Baccarat"
}


def get_game_state(values):
    msg = ""
    for val in values:
        if val["WinningHand"] == "Player":
            msg+="p"
        elif val["WinningHand"] == "Banker":
            msg+="b"
        elif val["WinningHand"] == "Tie":
            msg+="t"
    return msg

def get_stats(state):
    bank_count = 0
    player_count = 0
    tie_count = 0
    bank = 0
    player = 0
    tie = 0
    for g in state:
        if g == "b":
            bank_count+=1
            bank = 0
            player+=1
            tie+=1
        elif g == "p":
            player_count+=1
            player = 0
            bank+=1
            tie+=1
        elif g == "t":
            tie_count+=1
            tie = 0
            player+=1
            bank+=1
    return {"bank":bank,"player":player,"tie":tie,"bank_count":bank_count,"player_count":player_count,"tie_count":tie_count,"total_count":bank_count+player_count+tie_count}

def on_message(ws, message):
    try:
        json_data = json.loads(message)
        if json_data["MessageType"] == "UPDATED_LOBBY_DATA":
            if json_data["subMessageType"] == "UPDATED_TABLE_HISTORY":
                if json_data["gameType"] in ["2", "27", "20","21","24","25"]:
                    table_id = json_data["tableId"]
                    game_state = get_game_state(json_data["History"])
                    stats = get_stats(game_state)

                    rules = Rules()
                    rules.update_from_db()
                    rules.proc_bacc(table_id,"Ezugi " + BACCARAT_NAMES[table_id],stats)

                    db.update_bacca(table_id,game_state,stats)
            
    except Exception as e:
        pass





def on_open(ws):
    ws.send('{"MessageType":"LobbyInitializeDataByHome","ClientIP":"5.231.220.43","ClientId":"5555|1111_RUB|lobby","GameID":0,"Language":"ru","Nickid":"deadfox65","currentPlayerToken":"alalaa","OperatorID":5555,"SessionCurrency":"RUB","UID":"1111_RUB","clientType":"html"}')

# websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://engine.livetables.io/GameServer/lobby",
                              on_open = on_open,
                              on_message = on_message)
def parse_ezugi():
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            logger.error(e)
