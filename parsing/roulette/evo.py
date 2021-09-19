import websocket
import json
import time
import requests
import os

from loguru import logger
from roulette.roulette_parser import RouletteParser

ROUL_IDS= {
    'LightningTable01':1,
    'zosmk25g2f768o52':3,
    'wzg6kdkad1oe7m5k':[4,12],
    '7x0b1tgh7agmf6hv':5,
    'vctlz20yfnmp1ylr':6,
    'AmericanTable001':7,
    '01rb77cq1gtenhmo':8,
    '48z5pjps3ntvqc1b':9,
    'SpeedAutoRo00001':10,
    'f1f4rm9xgh4j3u2z':11,
    
    'r5aw9yumyaxgnd90':13,
    '8clwnwrupuvf0osq':14,
    'lkcbrbdckjxajdol':15,
    'qtkjorzrlqeb6hrd':16,
    'rr0yhns3we03tqqu':17,
    'mkvhbciosnfqhat7':18,
    'n4jwxsz2x4tqitvx':19,
    'otctxzr5fjyggijz':20,
    'o4vjrhh5rtwimgi3':21,
    'o44hwr2lc3a7spdh':22
}

class EvoParser(RouletteParser):
    """Парсер Эволюшн"""
    def start_parsing(self, on_parse):
        self.on_parse = on_parse
        while True:
            try:
                self.start_socket()
            except Exception as e:
                logger.error(e)
            time.sleep(5)
    def get_evo_id(self):
        return requests.get(os.environ.get('EVO_ID_URL')).text

    def get_data(self, message):
        json_data = json.loads(message)
        
        if not json_data["type"] == "lobby.rouletteNumbersUpdated":
            return None
        table_id = json_data["args"]["tableId"]
        if table_id not in ROUL_IDS:
            logger.info(f'{table_id} не в парсинге')
            return None
        ids = ROUL_IDS[table_id]
        if type(ids) is not list:
            ids = [ids]

        nums = []
        for num in json_data["args"]["numbers"]["results"]:
            if num[0]["number"] == "00":
                nozz_num = "0"
            else:
                nozz_num = num[0]["number"]
            nums.append(int(nozz_num))

        return{'ids':ids,'nums':nums}
    def on_message(self, ws, message):
        data = self.get_data(message)
        if not data:
            return
        for id in data['ids']:
            self.on_parse(id,data['nums'])
    def on_open(self, ws):
        table_strs = []
        for table_id in ROUL_IDS:
            table_strs.append('{"tableId":"'+table_id+'"}')
        ws.send('{"id":"youi1kqyew1","type":"lobby.updateSubscriptions","args":{"subscribeTopics":[{"topic":"table","tables":['+','.join(table_strs)+']}],"unsubscribeTopics":[]}}')
    def start_socket(self):
        evo_id = self.get_evo_id()
        ws = websocket.WebSocketApp(f"wss://marathonbet-com.evo-games.com/public/lobby/player/socket?messageFormat=json&EVOSESSIONID={evo_id}&client_version=6.20210406.71854.5551-09fabd4f4a",
            on_open = self.on_open,
            on_message = self.on_message)
        ws.run_forever()