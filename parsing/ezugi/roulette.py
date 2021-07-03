import websocket
import json

from db import db_main as db
from utils import roul_stats

ids = {'221000': 30,
        '221002': 31,
        '321000': 32,
        '221003': 33,
        '221004': 34,
        '431000': 35,
        '501000': 36,
        '611006': 37,
        '5001': 38,
        '611003': 39,
        '611004': 40,
        '611001': 41,
        '221005': 42,
        '411000': 43,
        '421000': 44,
        '1000': 45,
        '611005':46,
        '611000':47,
        # 'Slavyanka Roulette':48,
        '321001':49,
        '601000':50}


def check_and_print(data):
    if data["MessageType"] == "InitialData":
        for item in data["games"]:
            for game in item["popupList"]:
                if True or game['GameTypeID'] == "3" or game['GameTypeID'] == "29":
                    print(f"id {game['Tableid']}")
                    print(f"id {game['TableId']}")
                    print(f"type {game['GameTypeID']}")
                    print()
def get_new(old,new,off=6):
    for i in range(len(new) - off+1):
        if old[:off] == new[i:i+off]:
            return new[:i]
    return None
def on_message(ws, message):
    json_data = json.loads(message)
    
    # check_and_print(data)
    if json_data["MessageType"] == "UPDATED_LOBBY_DATA":
        if json_data["subMessageType"] == "UPDATED_TABLE_HISTORY":
            if json_data["tableId"] in ids:
                nums = []
                for num in json_data["History"][::-1]:
                    nums.append(int(num["WinningNumber"]))
                if len(nums)<10:
                    return
                new = {}
                datas = []
                id = ids[json_data["tableId"]]

                curr_nums = db.get_curr(id)

                if curr_nums == None:
                    print("1")
                    data = {"id":id,"action":'clear'}
                    datas.append(data)
                    if nums:
                        new[id] = nums
                else:
                    new_nums = get_new(curr_nums,nums)
                    if new_nums == None:
                        data = {"id":id,"action":'clear'}
                        datas.append(data)
                        if nums:
                            new[id] = nums
                    elif new_nums:
                        new[id] = new_nums
    for key in new:
        for number in new[key][::-1]:
            data = {"id":key,"value":int(number)}
            stats.add(key,int(number))
            datas.append(data)
    db.proc_datas(datas)
                
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"MessageType":"LobbyInitializeDataByHome","ClientIP":"5.231.220.43,"ClientId":"10424001|4446531_RUB|lobby","GameID":0,"Language":"ru","Nickid":"deadfox61","currentPlayerToken":"b97243ff-1bfa-46a0-967a-a983342882f4","OperatorID":10424001,"SessionCurrency":"RUB","UID":"4446531_RUB","clientType":"html"}')
    #ws.send('{"MessageType":"LobbyInitializeDataByHome","ClientIP":"85.202.228.123","ClientId":"5555|1111_RUB|lobby","GameID":0,"Language":"ru","Nickid":"deadfox65","currentPlayerToken":"alalaa","OperatorID":5555,"SessionCurrency":"RUB","UID":"1111_RUB","clientType":"html"}')

# websocket.enableTrace(True)
stats = roul_stats.RoulsStats()
stats.init_rouls()
ws = websocket.WebSocketApp("wss://engine.livetables.io/GameServer/lobby",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
def parse_ezugi():
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print(e)