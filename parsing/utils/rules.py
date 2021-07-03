from db import db_calc as db

class Rule():
    def __init__(self,rule_id, is_in_order,rule_type,count,user_id,is_zero, rouls_ids):
        self.rule_id = rule_id
        self.is_in_order = is_in_order
        self.rule_type = rule_type
        self.is_zero = is_zero
        """
        1 Red/Black
        2 Even/Odd
        3 Low/High
        4 дюжины
        5 колонки
        6 сектора по 3
        7 сектора по 6
        8 сектора рулетки
        9 череда
        10 число
        """
        self.count = count
        self.rouls_ids = rouls_ids
        self.user_id = user_id
        self.curr_add_msgs = []
        self.curr_stop_msgs = []
    def add_msg(self, stat_value, roul_name, stat_name):
        self.curr_add_msgs.append({"rule_id":self.rule_id,"user_id":self.user_id, "roul_name":roul_name, "is_in_order": self.is_in_order, "rule_name": stat_name, "count" : stat_value})
    def stop_msg(self, roul_name, stat_name):
        self.curr_stop_msgs.append({"rule_id":self.rule_id,"user_id":self.user_id, "roul_name":roul_name, "is_in_order": self.is_in_order, "rule_name": stat_name})
    def proc_msg(self,count,stat_value, roul_name, stat_name):
        if stat_value >= count:
            self.add_msg(stat_value, roul_name, stat_name)
        else:
            self.stop_msg(roul_name, stat_name)
    def update_msgs(self,roul_id,stats):
        self.curr_add_msgs = []
        self.curr_stop_msgs = []
        if stats.id not in self.rouls_ids:
            return
        if self.rule_type == 1:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.color.red.normal.zr_reset.value, stats.name, "red")
                    self.proc_msg(self.count,stats.color.black.normal.zr_reset.value, stats.name, "black")
                else:
                    self.proc_msg(self.count,stats.color.red.normal.zr_no_reset.value, stats.name, "red")
                    self.proc_msg(self.count,stats.color.black.normal.zr_no_reset.value, stats.name, "black")
            else:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.color.red.inverse.zr_reset.value, stats.name, "red")
                    self.proc_msg(self.count,stats.color.black.inverse.zr_reset.value, stats.name, "black")
                else:
                    self.proc_msg(self.count,stats.color.red.inverse.zr_no_reset.value, stats.name, "red")
                    self.proc_msg(self.count,stats.color.black.inverse.zr_no_reset.value, stats.name, "black")

        elif self.rule_type == 2:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.parity.odd.normal.zr_reset.value, stats.name, "odd")
                    self.proc_msg(self.count,stats.parity.even.normal.zr_reset.value, stats.name, "even")
                else:
                    self.proc_msg(self.count,stats.parity.odd.normal.zr_no_reset.value, stats.name, "odd")
                    self.proc_msg(self.count,stats.parity.even.normal.zr_no_reset.value, stats.name, "even")
            else:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.parity.odd.inverse.zr_reset.value, stats.name, "odd")
                    self.proc_msg(self.count,stats.parity.even.inverse.zr_reset.value, stats.name, "even")
                else:
                    self.proc_msg(self.count,stats.parity.odd.inverse.zr_no_reset.value, stats.name, "odd")
                    self.proc_msg(self.count,stats.parity.even.inverse.zr_no_reset.value, stats.name, "even")

        elif self.rule_type == 3:
            if self.is_in_order:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.bigness.big.normal.zr_reset.value, stats.name, "big")
                    self.proc_msg(self.count,stats.bigness.small.normal.zr_reset.value, stats.name, "small")
                else:
                    self.proc_msg(self.count,stats.bigness.big.normal.zr_no_reset.value, stats.name, "big")
                    self.proc_msg(self.count,stats.bigness.small.normal.zr_no_reset.value, stats.name, "small")
            else:
                if self.is_zero["fifty_fifty"]:
                    self.proc_msg(self.count,stats.bigness.big.inverse.zr_reset.value, stats.name, "big")
                    self.proc_msg(self.count,stats.bigness.small.inverse.zr_reset.value, stats.name, "small")
                else:
                    self.proc_msg(self.count,stats.bigness.big.inverse.zr_no_reset.value, stats.name, "big")
                    self.proc_msg(self.count,stats.bigness.small.inverse.zr_no_reset.value, stats.name, "small")

        elif self.rule_type == 4:
            if self.is_in_order:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        self.proc_msg(self.count,stats.dozen.data[i].normal.zr_reset.value, stats.name, f"dozen {i+1}")
                else:
                    for i in range(3):
                        self.proc_msg(self.count,stats.dozen.data[i].normal.zr_no_reset.value, stats.name, f"dozen {i+1}")
            else:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        self.proc_msg(self.count,stats.dozen.data[i].inverse.zr_reset.value, stats.name, f"dozen {i+1}")
                else:
                    for i in range(3):
                        self.proc_msg(self.count,stats.dozen.data[i].inverse.zr_no_reset.value, stats.name, f"dozen {i+1}")

        elif self.rule_type == 5:
            if self.is_in_order:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        self.proc_msg(self.count,stats.column.data[i].normal.zr_reset.value, stats.name, f"column {i+1}")
                else:
                    for i in range(3):
                        self.proc_msg(self.count,stats.column.data[i].normal.zr_no_reset.value, stats.name, f"column {i+1}")
            else:
                if self.is_zero["dozen_column"]:
                    for i in range(3):
                        self.proc_msg(self.count,stats.column.data[i].inverse.zr_reset.value, stats.name, f"column {i+1}")
                else:
                    for i in range(3):
                        self.proc_msg(self.count,stats.column.data[i].inverse.zr_no_reset.value, stats.name, f"column {i+1}")

        elif self.rule_type == 6:
            if self.is_in_order:
                for i in range(12):
                    self.proc_msg(self.count,stats.sector_3.data[i].normal.value, stats.name, f"sector {i*3+1}-{i*3+3}")
            else:
                for i in range(12):
                    self.proc_msg(self.count,stats.sector_3.data[i].inverse.value, stats.name, f"sector {i*3+1}-{i*3+3}")

        elif self.rule_type == 7:
            if self.is_in_order:
                for i in range(11):
                    self.proc_msg(self.count,stats.sector_6.data[i].normal.value, stats.name, f"sector {i*3+1}-{i*3+3}")
            else:
                for i in range(11):
                    self.proc_msg(self.count,stats.sector_6.data[i].inverse.value, stats.name, f"sector {i*3+1}-{i*3+6}")

        elif self.rule_type == 8:
            if self.is_in_order:
                self.proc_msg(self.count,stats.roul_sector.zero.normal.value, stats.name, "zero")
                self.proc_msg(self.count,stats.roul_sector.orphelins.normal.value, stats.name, "orphelins")
                self.proc_msg(self.count,stats.roul_sector.tiers.normal.value, stats.name, "tiers")
                self.proc_msg(self.count,stats.roul_sector.voisins.normal.value, stats.name, "voisins")
            else:
                self.proc_msg(self.count,stats.roul_sector.zero.inverse.value, stats.name, "zero")
                self.proc_msg(self.count,stats.roul_sector.orphelins.inverse.value, stats.name, "orphelins")
                self.proc_msg(self.count,stats.roul_sector.tiers.inverse.value, stats.name, "tiers")
                self.proc_msg(self.count,stats.roul_sector.voisins.inverse.value, stats.name, "voisins")
        elif self.rule_type == 9:
            if self.is_zero["alt_fifty_fifty"]:
                self.proc_msg(self.count,stats.color.alt.zr_reset.value, stats.name, "alt color")
                self.proc_msg(self.count,stats.parity.alt.zr_reset.value, stats.name, "alt parity")
                self.proc_msg(self.count,stats.bigness.alt.zr_reset.value, stats.name, "alt bigness")
            else:
                self.proc_msg(self.count,stats.color.alt.zr_no_reset.value, stats.name, "alt color")
                self.proc_msg(self.count,stats.parity.alt.zr_no_reset.value, stats.name, "alt parity")
                self.proc_msg(self.count,stats.bigness.alt.zr_no_reset.value, stats.name, "alt bigness")

            if self.is_zero["alt_dozen_column"]:
                self.proc_msg(self.count,stats.dozen.alt.zr_reset.value, stats.name, "alt dozen")
                self.proc_msg(self.count,stats.column.alt.zr_reset.value, stats.name, "alt column")
            else:
                self.proc_msg(self.count,stats.dozen.alt.zr_no_reset.value, stats.name, "alt dozen")
                self.proc_msg(self.count,stats.column.alt.zr_no_reset.value, stats.name, "alt column")
            self.proc_msg(self.count,stats.roul_sector.alt.value, stats.name, "alt sector")
        elif self.rule_type == 11:
            self.proc_msg(self.count,stats.sector_3.alt.value, stats.name, "alt sector 3")
        elif self.rule_type == 10:
            if self.is_in_order:
                for i in range(37):
                    self.proc_msg(self.count,stats.number.data[i].normal.value, stats.name, f"number {i}")
            else:
                for i in range(37):
                    self.proc_msg(self.count,stats.number.data[i].inverse.value, stats.name, f"number {i}")

class Rules():
    def __init__(self):
        self.rules = {}
    def init_rule(self, rule_id, is_in_order,rule_type,count,user_id, is_zero, rouls_ids):
        self.rules[rule_id] = Rule(rule_id, is_in_order,rule_type,count,user_id, is_zero, rouls_ids)
    def update_rules(self,rules_data):
        self.rules = {}
        for rule_data in rules_data:
            self.init_rule(rule_data["rule_id"],rule_data["is_in_order"],rule_data["rule_type"],rule_data["count"],rule_data["user_id"],rule_data["is_zero"],rule_data["rouls_ids"])
    def update_from_db(self):
        self.update_rules(db.get_rules())
    def proc_roul(self,roul_id,stats):
        add_msgs = []
        stop_msgs = []
        for rule_id in self.rules:
            self.rules[rule_id].update_msgs(roul_id,stats)
            add_msgs.extend(self.rules[rule_id].curr_add_msgs)
            stop_msgs.extend(self.rules[rule_id].curr_stop_msgs)
        self.db_apply(add_msgs,stop_msgs)
    def db_apply(self,add_msgs,stop_msgs):
        db.stop_msgs(stop_msgs)
        db.add_msgs(add_msgs)