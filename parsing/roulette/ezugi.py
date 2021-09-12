import websocket
import json
import time

from loguru import logger
from roulette.roulette_parser import RouletteParser


ROUL_IDS = {'221000': 30,
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


class EzugiParser(RouletteParser):
    """Парсер Езуги"""
    def start_parsing(self, on_parse):
        self.on_parse = on_parse
        while True:
            try:
                self.start_socket()
            except Exception as e:
                logger.error(e)
            time.sleep(5)

    def get_data(self, message):
        json_data = json.loads(message)
        if not (json_data["MessageType"] == "UPDATED_LOBBY_DATA" and json_data["subMessageType"] == "UPDATED_TABLE_HISTORY"):
            return None

        table_id = json_data["tableId"]
        if table_id not in ROUL_IDS:
            # logger.info(f'{table_id} not parsed')
            return None
        id = ROUL_IDS[table_id]

        nums = []
        for num in json_data["History"][::-1]:
            nums.append(int(num["WinningNumber"]))

        return{'id':id,'nums':nums}

    def on_message(self, ws, message):
        data = self.get_data(message)
        if not data:
            return
        self.on_parse(data['id'],data['nums'])

    def on_open(self, ws):
        ws.send('{"MessageType":"LobbyInitializeDataByHome","ClientIP":"5.231.220.43,"ClientId":"10424001|4446531_RUB|lobby","GameID":0,"Language":"ru","Nickid":"deadfox61","currentPlayerToken":"b97243ff-1bfa-46a0-967a-a983342882f4","OperatorID":10424001,"SessionCurrency":"RUB","UID":"4446531_RUB","clientType":"html"}')

    def start_socket(self):
        ws = websocket.WebSocketApp("wss://engine.livetables.io/GameServer/lobby",
            on_open = self.on_open,
            on_message = self.on_message)
        ws.run_forever()