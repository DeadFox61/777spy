from db import db_calc as db

from roulette.main_stats import RoulsStats
from roulette.personal_stats import IndRoulStats

class Msgs():
    """Класс сообщений"""
    def __init__(self, rule):
        self.add_msgs = []
        self.stop_msgs = []
        self.rule = rule

    def add_msg(self, stat_value, roul_name, stat_name):
        self.add_msgs.append({"rule_id":self.rule.rule_id,"user_id":self.rule.user_id, "roul_name":roul_name, "is_in_order": self.rule.is_in_order, "rule_name": stat_name, "count" : stat_value})
    def stop_msg(self, roul_name, stat_name):
        self.stop_msgs.append({"rule_id":self.rule.rule_id,"user_id":self.rule.user_id, "roul_name":roul_name, "is_in_order": self.rule.is_in_order, "rule_name": stat_name})
    def proc_msg(self,stat_value, roul_name, stat_name, is_max = False):
        if stat_value == None:
            return
        if is_max:
            is_in_rule = stat_value >= self.rule.count and stat_value <= self.rule.max_count
        else:
            is_in_rule = stat_value >= self.rule.count
        if is_in_rule:
            self.add_msg(stat_value, roul_name, stat_name)
        else:
            self.stop_msg(roul_name, stat_name)

    def get_add_msgs(self):
        """Возвращает сообщения, которые нужно отправить"""
        return self.add_msgs

    def get_stop_msgs(self):
        """Возвращает сообщения, которые нужно остановить"""
        return self.stop_msgs

class Rule():
    """Класс правила"""
    def __init__(self, stats, rule_data):
        self.stats = stats
        self.rule_id = rule_data['rule_id']
        self.is_in_order = rule_data['is_in_order']
        self.rule_type = rule_data['rule_type']
        """
        1 Red/Black
        2 Even/Odd
        3 Low/High
        4 дюжины
        5 колонки
        6 сектора по 3
        7 сектора по 6
        8 сектора рулетки
        9 череда кроме секторов по 3
        11 череда секторов по 3
        10 число
        101 fav
        """
        self.is_zero = rule_data['is_zero']
        self.count = rule_data['count']
        self.max_count = rule_data['max_count']
        self.rouls_ids = rule_data['rouls_ids']
        self.user_id = rule_data['user_id']

    def get_msgs(self, roul_id):
        """Возвращает список сообщений по этому правилу для рулетки roul_id"""
        msgs = Msgs(self)
        if roul_id not in self.rouls_ids:
            return
        if self.rule_type == 1:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.red.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "red")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.black.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "black")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.red.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "red")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.black.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "black")
            else:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.red.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "red")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.black.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "black")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.red.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "red")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.black.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "black")

        elif self.rule_type == 2:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.odd.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "odd")
                    msgs.proc_msg(self.count,stats.parity.even.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "even")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.odd.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "odd")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.even.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "even")
            else:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.odd.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "odd")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.even.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "even")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.odd.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "odd")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.even.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "even")

        elif self.rule_type == 3:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.big.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "big")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.small.normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "small")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.big.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "big")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.small.normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "small")
            else:
                if self.is_zero["fifty_fifty"]:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.big.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "big")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.small.inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "small")
                else:
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.big.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "big")
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.small.inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "small")

        elif self.rule_type == 4:
            if self.is_in_order:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.data[i].normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"dozen {i+1}")
                else:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.data[i].normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"dozen {i+1}")
            else:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.data[i].inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"dozen {i+1}")
                else:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.data[i].inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"dozen {i+1}")

        elif self.rule_type == 5:
            if self.is_in_order:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.data[i].normal.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"column {i+1}")
                else:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.data[i].normal.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"column {i+1}")
            else:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.data[i].inverse.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"column {i+1}")
                else:
                    for i in range(3):
                        msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.data[i].inverse.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, f"column {i+1}")

        elif self.rule_type == 6:
            if self.is_in_order:
                for i in range(12):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).sector_3.data[i].normal.value, self.stats.main_stats.get_stats(roul_id).name, f"sector {i*3+1}-{i*3+3}")
            else:
                for i in range(12):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).sector_3.data[i].inverse.value, self.stats.main_stats.get_stats(roul_id).name, f"sector {i*3+1}-{i*3+3}")

        elif self.rule_type == 7:
            if self.is_in_order:
                for i in range(11):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).sector_6.data[i].normal.value, self.stats.main_stats.get_stats(roul_id).name, f"sector {i*3+1}-{i*3+3}")
            else:
                for i in range(11):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).sector_6.data[i].inverse.value, self.stats.main_stats.get_stats(roul_id).name, f"sector {i*3+1}-{i*3+6}")

        elif self.rule_type == 8:
            if self.is_in_order:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.zero.normal.value, self.stats.main_stats.get_stats(roul_id).name, "zero")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.orphelins.normal.value, self.stats.main_stats.get_stats(roul_id).name, "orphelins")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.tiers.normal.value, self.stats.main_stats.get_stats(roul_id).name, "tiers")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.voisins.normal.value, self.stats.main_stats.get_stats(roul_id).name, "voisins")
            else:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.zero.inverse.value, self.stats.main_stats.get_stats(roul_id).name, "zero")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.orphelins.inverse.value, self.stats.main_stats.get_stats(roul_id).name, "orphelins")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.tiers.inverse.value, self.stats.main_stats.get_stats(roul_id).name, "tiers")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.voisins.inverse.value, self.stats.main_stats.get_stats(roul_id).name, "voisins")
        elif self.rule_type == 9:
            if self.is_zero["alt_fifty_fifty"]:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.alt.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt color")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.alt.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt parity")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.alt.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt bigness")
            else:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).color.alt.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt color")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).parity.alt.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt parity")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).bigness.alt.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt bigness")

            if self.is_zero["alt_dozen_column"]:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.alt.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt dozen")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.alt.zr_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt column")
            else:
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).dozen.alt.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt dozen")
                msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).column.alt.zr_no_reset.value, self.stats.main_stats.get_stats(roul_id).name, "alt column")
            msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).roul_sector.alt.value, self.stats.main_stats.get_stats(roul_id).name, "alt sector")
        elif self.rule_type == 11:
            msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).sector_3.alt.value, self.stats.main_stats.get_stats(roul_id).name, "alt sector 3")
        elif self.rule_type == 10:
            if self.is_in_order:
                for i in range(37):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).number.data[i].normal.value, self.stats.main_stats.get_stats(roul_id).name, f"number {i}")
            else:
                for i in range(37):
                    msgs.proc_msg(self.stats.main_stats.get_stats(roul_id).number.data[i].inverse.value, self.stats.main_stats.get_stats(roul_id).name, f"number {i}")

        # Правила на основе индивидуальной статистики
        elif self.rule_type == 101:
            msgs.proc_msg(self.stats.ind_stats.get_stats(self.user_id,roul_id).fav_num.value, self.stats.controller.get_full_name(roul_id), f"fav", True)

        return msgs



class Rules():
    def __init__(self, stats):
        self.stats = stats
        self.rules = {}

    def update_rules(self):
        """Обновляет список правил из бд"""
        rules_data = db.get_rules()
        self.rules = {}
        for rule_data in rules_data:
            self.rules[rule_data["rule_id"]] =  Rule(self.stats, rule_data)

    def proc_rules(self, roul_id):
        """Обрабатывает правила для рулетки roul_id"""
        self.update_rules()
        add_msgs = []
        stop_msgs = []
        for rule_id in self.rules:
            msgs = self.rules[rule_id].get_msgs(roul_id)
            if msgs:
                add_msgs.extend(msgs.get_add_msgs())
                stop_msgs.extend(msgs.get_stop_msgs())
        db.stop_msgs(stop_msgs)
        db.add_msgs(add_msgs)