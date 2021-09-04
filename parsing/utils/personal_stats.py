from db import db_calc as db


class FavNumRoulStat():
    """Класс статистики среднего невыпадения любимых чисел юзера"""
    def __init__(self,checked_nums):
        # Количество невыпадений подряд
        self.nums_stats = {}
        self.value = 0
        for checked_num in checked_nums:
            self.nums_stats[checked_num] = 0
    def add_num(self,num):
        if self.nums_stats:
            num_sum = 0
            num_count = 0
            for checked_num in self.nums_stats:
                if num == checked_num:
                    self.nums_stats[checked_num] = 0
                else:
                    self.nums_stats[checked_num] += 1
                num_sum += self.nums_stats[checked_num]
                num_count += 1
            self.value = round(num_sum/num_count)
        else:
            self.value = 0
    def to_json(self):
        return self.value

class IndUserRoulStat():
    """Класс индивидуальной статистики """
    def __init__(self,user_data):
        self.fav_num = FavNumRoulStat(user_data.get("checked_nums"))
    def add_num(self, num):
        self.fav_num.add_num(num)
    def to_json(self):
        res = {}
        res['fav_num'] = self.fav_num.to_json()
        return res

class IndUserRoulsStats():
    """Класс ститистики по всем рулеткам для юзера user_id"""
    def __init__(self,user_id, user_data):
        self.user_id = user_id
        self.load_data(user_data)
    def load_data(self,user_data):
        self.data = {}
        self.roul_ids = user_data['rouls_ids']
        self.raw_data = user_data['data']
        for roul_id in self.roul_ids:
            self.data[roul_id] = IndUserRoulStat(user_data['data'])
    def add_num(self,roul_id,num,is_save=True):
        if roul_id not in self.data:
            return
        self.data[roul_id].add_num(num)
        if is_save:
            self.save()
    def to_json(self):
        res = {}
        for roul_id in self.data:
            res[roul_id] = self.data[roul_id].to_json()
        return res
    def check_updates(self, user_data):
        """Проверяет, менял ли юзер с self.user_id свои настройки"""
        if user_data['rouls_ids'] != self.roul_ids or user_data['data'] != self.raw_data:
            print(f'{self.user_id} был изменён!')
            self.reload(user_data)
    def reload(self, user_data):
        """Перезагружает настройки и пересчитывает статистику"""
        self.load_data(user_data)
    def save(self):
        db.ind_save_stat(self.user_id, self.to_json())


class IndRoulStats():
    """Класс индивидуальной статистики"""
    def __init__(self):
        self.data = {}
    def load_data(self,from_db = True, users_data=None):
        self.data = {}
        if from_db:
            users_data = db.get_users_data()
        for user_id in users_data:
            self.data[user_id] = IndUserRoulsStats(user_id, users_data[user_id])
    def check_updates(self):
        users_data = db.get_users_data()
        for user_id in users_data:
            if user_id not in self.data:
                self.data[user_id] = IndUserRoulsStats(user_id, users_data[user_id])
            else:
                self.data[user_id].check_updates(users_data[user_id])
    def add_num(self, roul_id, num):
        for user_id in self.data:
            self.data[user_id].add_num(roul_id, num)
    def add_nums(self, roul_id, nums):
        for num in nums:
            self.add_num(roul_id, num)