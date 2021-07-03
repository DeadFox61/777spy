import websocket
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time

import db
import roul_stats

#'wzg6kdkad1oe7m5k':4,12
ROUL_IDS= {
    'LightningTable01':1,
    'zosmk25g2f768o52':3,
    
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

def nice_print_baccarat(values):
    msg=""
    for val in values:
        if val["color"] == "Red":
            msg+="r"
        else:
            msg+="b"
        msg+="g"*val["ties"]
    print(msg)
def nice_print_roul(values):
    msg=""
    for val in values:
        msg+=str(val[0]["number"])+" "
    print(msg)

def get_new(old,new,off=6):
    for i in range(len(new) - off+1):
        if old[:off] == new[i:i+off]:
            return new[:i]
    return None

def on_message(ws, message):
    try:
        json_data = json.loads(message)
        if json_data["type"] == "lobby.rouletteNumbersUpdated":
            print("panel")
            print(json_data["args"]["tableId"])
            nice_print_roul(json_data["args"]["numbers"]["results"])
            nums = []
            for num in json_data["args"]["numbers"]["results"]:
                
                if num[0]["number"] == "00":
                    nozz_num = "0"
                else:
                    nozz_num = num[0]["number"]
                nums.append(int(nozz_num))
            new = {}
            datas = []
            
            if json_data["args"]["tableId"] == "wzg6kdkad1oe7m5k":
                ids = [4,12]
            else:
                ids = [ROUL_IDS[json_data["args"]["tableId"]]]    
            for id in ids:
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
    except Exception as e:
        print(e)

               
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('''{"id":"youi1kqyew1","type":"lobby.updateSubscriptions","args":{"subscribeTopics":[{"topic":"table","tables":[
{"tableId":"LightningTable01"},
{"tableId":"otctxzr5fjyggijz"},
{"tableId":"zosmk25g2f768o52"},
{"tableId":"wzg6kdkad1oe7m5k"},
{"tableId":"7x0b1tgh7agmf6hv"},
{"tableId":"vctlz20yfnmp1ylr"},
{"tableId":"AmericanTable001"},
{"tableId":"01rb77cq1gtenhmo"},
{"tableId":"48z5pjps3ntvqc1b"},
{"tableId":"SpeedAutoRo00001"},
{"tableId":"f1f4rm9xgh4j3u2z"},
{"tableId":"wzg6kdkad1oe7m5k","vtId":"ojn3tdth6fkinkmp"},
{"tableId":"r5aw9yumyaxgnd90"},
{"tableId":"8clwnwrupuvf0osq"},
{"tableId":"lkcbrbdckjxajdol"},
{"tableId":"qtkjorzrlqeb6hrd"},
{"tableId":"mkvhbciosnfqhat7"},
{"tableId":"n4jwxsz2x4tqitvx"},
{"tableId":"rr0yhns3we03tqqu"},
{"tableId":"o4vjrhh5rtwimgi3"},
{"tableId":"o44hwr2lc3a7spdh"}
]}],"unsubscribeTopics":[]}}''')

def start_socket():
    #websocket.enableTrace(True)
    evo_id = db.get_evo_id()
    ws = websocket.WebSocketApp(f"wss://marathonbet-com.evo-games.com/public/lobby/player/socket?messageFormat=json&EVOSESSIONID={evo_id}&client_version=6.20210406.71854.5551-09fabd4f4a",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()

if __name__ == "__main__":
    stats = roul_stats.RoulsStats()
    stats.init_rouls()
    while True:
        try:
            start_socket()
        except Exception as e:
            print(e)
