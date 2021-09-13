from db import db_calc as db

class Rule():
    def __init__(self,rule_id, rule_type,count,user_id, baccs_ids):
        self.rule_id = rule_id
        self.rule_type = rule_type
        """
        1 Bank
        2 Player
        3 Tie
        """
        self.count = count
        self.baccs_ids = baccs_ids
        self.user_id = user_id
        self.curr_add_msgs = []
        self.curr_stop_msgs = []
    def add_msg(self, stat_value, bacc_name, stat_name):
        self.curr_add_msgs.append({"rule_id":self.rule_id,"user_id":self.user_id, "bacc_name":bacc_name, "rule_name": stat_name, "count" : stat_value})
    def stop_msg(self, bacc_name, stat_name):
        self.curr_stop_msgs.append({"rule_id":self.rule_id,"user_id":self.user_id, "bacc_name":bacc_name, "rule_name": stat_name})
    def proc_msg(self,count,stat_value, bacc_name, stat_name):
        if stat_value >= count:
            self.add_msg(stat_value, bacc_name, stat_name)
        else:
            self.stop_msg(bacc_name, stat_name)
    def update_msgs(self,bacc_id,bacc_name,stats):
        self.curr_add_msgs = []
        self.curr_stop_msgs = []
        if bacc_id not in self.baccs_ids:
            return
        if self.rule_type == 1:
            self.proc_msg(self.count,stats["bank"], bacc_name, "Bank")
        elif self.rule_type == 2:
            self.proc_msg(self.count,stats["player"], bacc_name, "Player")
        elif self.rule_type == 3:
            self.proc_msg(self.count,stats["tie"], bacc_name, "Tie")

class Rules():
    def __init__(self):
        self.rules = {}
    def init_rule(self, rule_id ,rule_type,count,user_id, baccs_ids):
        self.rules[rule_id] = Rule(rule_id,rule_type,count,user_id,  baccs_ids)
    def update_rules(self,rules_data):
        self.rules = {}
        for rule_data in rules_data:
            self.init_rule(rule_data["rule_id"],rule_data["rule_type"],rule_data["count"],rule_data["user_id"],rule_data["baccs_ids"])
    def update_from_db(self):
        self.update_rules(db.get_rules_bacc())
    def proc_bacc(self,bacc_id, bacc_name, stats):
        add_msgs = []
        stop_msgs = []
        for rule_id in self.rules:
            self.rules[rule_id].update_msgs(bacc_id, bacc_name, stats)
            add_msgs.extend(self.rules[rule_id].curr_add_msgs)
            stop_msgs.extend(self.rules[rule_id].curr_stop_msgs)
        self.db_apply(add_msgs,stop_msgs)
    def db_apply(self,add_msgs,stop_msgs):
        db.stop_msgs_bacc(stop_msgs)
        db.add_msgs_bacc(add_msgs)