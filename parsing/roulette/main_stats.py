from db import db_calc as db
import time

from roulette.main_rules import Rules
from loguru import logger

NUM_RED = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

ZERO_SEC = [0, 3, 12, 15, 26, 32, 35]
ORPHELINS_SEC = [1, 6, 9, 14, 17, 20, 31, 34]
TIERS_SEC = [5, 8, 10, 11, 13, 16, 23, 24, 27, 30, 33, 36]
VOISINS_SEC = [0, 3, 12, 15, 26, 32, 35, 2, 4, 7, 18, 19, 21, 22, 25, 28, 29]
ANGLES_SECS = [
    [0, 1, 2], [0, 2, 3],[1, 2, 4, 5], [2, 3, 5, 6], 
    [4, 5, 7, 8], [5, 6, 8, 9],[7, 8, 10, 11], [8, 9, 11, 12],
    [10, 11, 13, 14], [11, 12, 14, 15], [13, 14, 16, 17], [14, 15, 17, 18],
    [16, 17, 19, 20], [17, 18, 20, 21], [19, 20, 22, 23], [20, 21, 23, 24],
    [22, 23, 25, 26], [23, 24, 26, 27], [25, 26, 28, 29], [26, 27, 29, 30],
    [28, 29, 31, 32], [29, 30, 32, 33], [31, 32, 34, 35], [32, 33, 35, 36]
]

class BasicStat():
    def __init__(self,value = 0):
        self.value = value
    def add_one(self):
        self.value+=1
    def reset(self):
        self.value = 0
class BasicStatZr():
    def __init__(self):
        self.zr_reset = BasicStat()
        self.zr_no_reset = BasicStat()
    def add_one(self):
        self.zr_reset.add_one()
        self.zr_no_reset.add_one()
    def reset(self):
        self.zr_reset.reset()
        self.zr_no_reset.reset()
    def zero_reset(self):
        self.zr_reset.reset()
        self.zr_no_reset.add_one()
    def to_json(self):
        res = {}
        res["zr_reset"] = self.zr_reset.value
        res["zr_no_reset"] = self.zr_no_reset.value
        return res

class AltStat():
    def __init__(self,value = 0, last = None):
        self.value = value
        self.last = last
    def apply(self,el):
        if el == self.last:
            self.value = 0
        else:
            self.last = el
            self.value += 1
    def reset(self):
        self.value = 0
        self.last = None
    def to_json(self):
        return self.value
class AltStatZr():
    def __init__(self):
        self.zr_reset = AltStat()
        self.zr_no_reset = AltStat()
    def apply(self,el):
        self.zr_reset.apply(el)
        self.zr_no_reset.apply(el)
    def zero_reset(self):
        self.zr_reset.reset()
        self.zr_no_reset.apply(0)
    def to_json(self):
        res = {}
        res["zr_reset"] = self.zr_reset.value
        res["zr_no_reset"] = self.zr_no_reset.value
        return res

class CombStat():
    def __init__(self):
        self.normal = BasicStat()
        self.inverse = BasicStat()
    def add_one(self):
        self.normal.add_one()
        self.inverse.reset()
    def reset(self):
        self.inverse.add_one()
        self.normal.reset()
    def apply(self,is_good):
        if is_good:
            self.add_one()
        else:
            self.reset()
    def to_json(self):
        res = {}
        res["normal"] = self.normal.value
        res["inverse"] = self.inverse.value
        return res

class CombStatZr():
    def __init__(self):
        self.normal = BasicStatZr()
        self.inverse = BasicStatZr()
    def zero_reset(self):
        self.normal.zero_reset()
        self.inverse.zero_reset()
    def add_one(self):
        self.normal.add_one()
        self.inverse.reset()
    def reset(self):
        self.inverse.add_one()
        self.normal.reset()
    def apply(self,is_good):
        if is_good:
            self.add_one()
        else:
            self.reset()
    def to_json(self):
        res = {}
        res["normal"] = self.normal.to_json()
        res["inverse"] = self.inverse.to_json()
        return res
# Классы статов
class Color():
    def __init__(self):
        self.red = CombStatZr()
        self.black = CombStatZr()
        self.alt = AltStatZr()
    def add(self,num):
        if num == 0:
            self.red.zero_reset()
            self.black.zero_reset()
            self.alt.zero_reset()
        else:
            is_red = num in NUM_RED
            self.red.apply(is_red)
            self.black.apply(not is_red)
            self.alt.apply(is_red)
    def to_json(self):
        res = {}
        res["red"] = self.red.to_json()
        res["black"] = self.black.to_json()
        res["alt"] = self.alt.to_json()
        return res

class Parity():
    def __init__(self):
        self.odd = CombStatZr()
        self.even = CombStatZr()
        self.alt = AltStatZr()
    def add(self,num):
        if num == 0:
            self.odd.zero_reset()
            self.even.zero_reset()
            self.alt.zero_reset()
        else:
            is_even = num % 2 == 0
            self.odd.apply(not is_even)
            self.even.apply(is_even)
            self.alt.apply(is_even)
    def to_json(self):
        res = {}
        res["odd"] = self.odd.to_json()
        res["even"] = self.even.to_json()
        res["alt"] = self.alt.to_json()
        return res

class Bigness():
    def __init__(self):
        self.big = CombStatZr()
        self.small = CombStatZr()
        self.alt = AltStatZr()
    def add(self,num):
        if num == 0:
            self.big.zero_reset()
            self.small.zero_reset()
            self.alt.zero_reset()
        else:
            is_big = num > 18
            self.big.apply(is_big)
            self.small.apply(not is_big)
            self.alt.apply(is_big)
    def to_json(self):
        res = {}
        res["big"] = self.big.to_json()
        res["small"] = self.small.to_json()
        res["alt"] = self.alt.to_json()
        return res

class Dozen():
    def __init__(self):
        self.data = []
        for i in range(3):
            self.data.append(CombStatZr())
        self.alt = AltStatZr()
    def add(self,num):
        if num == 0:
            for i in range(3):
                self.data[i].zero_reset()
            self.alt.zero_reset()
        else:
            dozen = (num-1) // 12
            for i in range(3):
                self.data[i].apply(i == dozen)
            self.alt.apply(dozen)
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(3):
            res["data"].append(self.data[i].to_json())
        res["alt"] = self.alt.to_json()
        return res

class Column():
    def __init__(self):
        self.data = []
        for i in range(3):
            self.data.append(CombStatZr())
        self.alt = AltStatZr()
    def add(self,num):
        if num == 0:
            for i in range(3):
                self.data[i].zero_reset()
            self.alt.zero_reset()
        else:
            column = (num-1) % 3 
            for i in range(3):
                self.data[i].apply(i == column)
            self.alt.apply(column)
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(3):
            res["data"].append(self.data[i].to_json())
        res["alt"] = self.alt.to_json()
        return res

class RoulSector():
    def __init__(self):
        self.zero = CombStat()
        self.orphelins = CombStat()
        self.tiers = CombStat()
        self.voisins = CombStat()
        self.alt = AltStat()
    def add(self,num):
        self.zero.apply(num in ZERO_SEC)
        self.orphelins.apply(num in ORPHELINS_SEC)
        self.tiers.apply(num in TIERS_SEC)
        self.voisins.apply(num in VOISINS_SEC)
        if num in ORPHELINS_SEC:
            self.alt.apply("orph")
        elif num in TIERS_SEC:
            self.alt.apply("tiers")
        elif num in VOISINS_SEC:
            self.alt.apply("voisins")
    def to_json(self):
        res = {}
        res["zero"] = self.zero.to_json()
        res["orphelins"] = self.orphelins.to_json()
        res["tiers"] = self.tiers.to_json()
        res["voisins"] = self.voisins.to_json()
        res["alt"] = self.alt.to_json()
        return res
class Sector3():
    def __init__(self):
        self.data = []
        for i in range(12):
            self.data.append(CombStat())
        self.alt = AltStat()
    def add(self,num):
        for i in range(12):
            self.data[i].apply(num!=0 and i == (num-1) // 3)
        self.alt.apply((num-1) // 3)
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(12):
            res["data"].append(self.data[i].to_json())
        res["alt"] = self.alt.to_json()
        return res
class Sector6():
    def __init__(self):
        self.data = []
        for i in range(11):
            self.data.append(CombStat())
    def add(self,num):
        ind = (num-1) // 3
        for i in range(11):
            self.data[i].apply(num!=0 and i == ind-1 or i == ind)
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(11):
            res["data"].append(self.data[i].to_json())
        return res
class Number():
    def __init__(self):
        self.data = []
        for i in range(37):
            self.data.append(CombStat())
    def add(self,num):
        for i in range(37):
            self.data[i].apply(i == num)
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(37):
            res["data"].append(self.data[i].to_json())
        return res
class Angle():
    def __init__(self):
        self.data = []
        for i in range(24):
            self.data.append(CombStat())
    def add(self,num):
        for i in range(24):
            self.data[i].apply(num in ANGLES_SECS[i])
    def to_json(self):
        res = {}
        res["data"] = []
        for i in range(24):
            res["data"].append(self.data[i].to_json())
        return res


class RoulStats():
    def __init__(self, roul_id, name, nums = []):
        self.roul_id = roul_id
        if self.roul_id>29:
            prod = "Ezugi"
        else:
            prod = "EG"
        self.name = f"{prod} {name}"
        self.nums = []
        self.color = Color()
        self.parity = Parity()
        self.bigness = Bigness()
        self.dozen = Dozen()
        self.column = Column()
        self.roul_sector = RoulSector()
        self.sector_3 = Sector3()
        self.sector_6 = Sector6()
        self.number = Number()
        self.angle = Angle()
        self.add_nums(nums)
    def add_num(self,num):
        self.color.add(num)
        self.parity.add(num)
        self.bigness.add(num)
        self.dozen.add(num)
        self.column.add(num)
        self.roul_sector.add(num)
        self.sector_3.add(num)
        self.sector_6.add(num)
        self.number.add(num)
        self.angle.add(num)
    def add_nums(self,nums):
        for num in nums[::-1]:
            self.add_num(num)
    def to_json(self):
        res = {}
        res["color"] = self.color.to_json()
        res["parity"] = self.parity.to_json()
        res["bigness"] = self.bigness.to_json()
        res["dozen"] = self.dozen.to_json()
        res["column"] = self.column.to_json()
        res["roul_sector"] = self.roul_sector.to_json()
        res["sector_3"] = self.sector_3.to_json()
        res["sector_6"] = self.sector_6.to_json()
        res["number"] = self.number.to_json()
        res["angle"] = self.angle.to_json()
        return res
    def save(self):
        json_stats = self.to_json()
        db.save_stat(self.roul_id,json_stats)
class RoulsStats():
    def __init__(self):
        self.rouls = {}
        self.rules = Rules()
    def init_roul(self, roul_id, name, nums):
        if roul_id not in self.rouls:
            roul = RoulStats(roul_id = roul_id, name = name)
            roul.add_nums(nums)
            self.rouls[roul_id] = roul
    def reload_roul(self, roul_id, name, nums):
        if roul_id in self.rouls:
            self.rouls[roul_id] = RoulStats(roul_id = roul_id, name = name)
            self.rouls[roul_id].add_nums(nums)
            self.rouls[roul_id].save()
    def init_rouls(self, roul_data):
        for roul_id in roul_data:
            self.init_roul(roul_id,roul_data[roul_id]["name"],roul_data[roul_id]["nums"])
    def add(self, roul_id, num):
        try:
            self.rouls[roul_id].add_num(num)
            self.rouls[roul_id].save()
            self.rules.update_from_db()
            self.rules.proc_roul(roul_id,self.rouls[roul_id])
        except Exception as e:
            logger.error(e)
