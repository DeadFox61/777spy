import websocket
import json
import time
import requests
from loguru import logger
import os

from db import db_main as db
from utils.rules_bacc import Rules

BACCARAT_NAMES = {
    "leqhceumaq6qfoug": "Speed Baccarat A",
    "lv2kzclunt2qnxo5": "Speed Baccarat B",
    "ndgvwvgthfuaad3q": "Speed Baccarat C",
    "ndgvz5mlhfuaad6e": "Speed Baccarat D",
    "ndgv45bghfuaaebf": "Speed Baccarat E",
    "nmwde3fd7hvqhq43": "Speed Baccarat F",
    "nmwdzhbg7hvqh6a7": "Speed Baccarat G",
    "nxpj4wumgclak2lx": "Speed Baccarat H",
    "nxpkul2hgclallno": "Speed Baccarat I",
    "obj64qcnqfunjelj": "Speed Baccarat J",
    "ocye2ju2bsoyq6vv": "Speed Baccarat K",
    "ovu5cwp54ccmymck": "Speed Baccarat L",
    "ovu5dsly4ccmynil": "Speed Baccarat M",
    "ovu5eja74ccmyoiq": "Speed Baccarat N",
    "ovu5fbxm4ccmypmb": "Speed Baccarat O",
    "ovu5fzje4ccmyqnr": "Speed Baccarat P",
    "o4kyj7tgpwqqy4m4": "Speed Baccarat Q",
    "NoCommBac0000001": "No Commission Baccarat",
    "ndgv76kehfuaaeec": "No Commission Speed Baccarat A",
    "ocye5hmxbsoyrcii": "No Commission Speed Baccarat B",
    "ovu5h6b3ujb4y53w": "No Commission Speed Baccarat C",
    "LightningBac0001": "Lightning Baccarat",
    "k2oswnib7jjaaznw": "Baccarat Control Squeeze",
    "zixzea8nrf1675oh": "Baccarat Squeeze",
    "oytmvb9m1zysmc44": "Baccarat A",
    "60i0lcfx5wkkv3sy": "Baccarat B",
    "ndgvs3tqhfuaadyg": "Baccarat C"
}

def get_evo_id():
    return requests.get(os.environ.get('EVO_ID_URL')).text

def get_game_state(values):
    msg=""
    for val in values:
        if val["color"] == "Red":
            msg+="b"
        else:
            msg+="p"
        msg+="t"*val["ties"]
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
        if json_data['type'] == 'lobby.baccaratRoadUpdated':
            table_id = json_data["args"]["tableId"]
            game_state = get_game_state(json_data["args"]["bigRoad"])
            stats = get_stats(game_state)

            rules = Rules()
            rules.update_from_db()
            rules.proc_bacc(table_id,"EG " + BACCARAT_NAMES[table_id],stats)

            db.update_bacca(table_id,game_state,stats)
            
    except Exception as e:
        logger.error(e)

def on_open(ws):
    ws.send('''{"id":"youi1kqyew1","type":"lobby.updateSubscriptions","args":{"subscribeTopics":[{"topic":"table","tables":[
{"tableId": "SuperSicBo000001"} 
,{"tableId": "DragonTiger00001"} 
,{"tableId": "leqhceumaq6qfoug"}
,{"tableId": "lv2kzclunt2qnxo5"}
,{"tableId": "ndgvwvgthfuaad3q"}
,{"tableId": "ndgvz5mlhfuaad6e"}
,{"tableId": "ndgv45bghfuaaebf"}
,{"tableId": "nmwde3fd7hvqhq43"}
,{"tableId": "nmwdzhbg7hvqh6a7"}
,{"tableId": "nxpj4wumgclak2lx"}
,{"tableId": "nxpkul2hgclallno"}
,{"tableId": "obj64qcnqfunjelj"}
,{"tableId": "ocye2ju2bsoyq6vv"}
,{"tableId": "ovu5cwp54ccmymck"}
,{"tableId": "ovu5dsly4ccmynil"}
,{"tableId": "ovu5eja74ccmyoiq"}
,{"tableId": "ovu5fbxm4ccmypmb"}
,{"tableId": "ovu5fzje4ccmyqnr"}
,{"tableId": "o4kyj7tgpwqqy4m4"}
,{"tableId": "NoCommBac0000001"}
,{"tableId": "ndgv76kehfuaaeec"}
,{"tableId": "ocye5hmxbsoyrcii"}
,{"tableId": "ovu5h6b3ujb4y53w"}
,{"tableId": "LightningBac0001"}
,{"tableId": "k2oswnib7jjaaznw"}
,{"tableId": "zixzea8nrf1675oh"}
,{"tableId": "oytmvb9m1zysmc44"}
,{"tableId": "60i0lcfx5wkkv3sy"}
,{"tableId": "ndgvs3tqhfuaadyg"}
]}],"unsubscribeTopics":[]}}''')

def start_socket():
    #websocket.enableTrace(True)
    evo_id = get_evo_id()
    ws = websocket.WebSocketApp(f"wss://marathonbet-com.evo-games.com/public/lobby/player/socket?messageFormat=json&EVOSESSIONID={evo_id}&client_version=6.20210406.71854.5551-09fabd4f4a",
                              on_open = on_open,
                              on_message = on_message)

    ws.run_forever()


def parse_evo():
    while True:
        try:
            start_socket()
        except Exception as e:
            logger.error(e)
