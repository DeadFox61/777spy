from roulette.main_stats import RoulsStats
from roulette.personal_stats import IndRoulStats
from roulette.rules import Rules


class Stats():
    """Класс управления статистикой"""
    def __init__(self, controller):
        self.controller = controller
        self.main_stats = RoulsStats(controller)
        self.ind_stats = IndRoulStats(controller)
        self.rules = Rules(self)

    def add_num(self, roul_id, num):
        """Добавляет одно число в рулетку"""
        self.main_stats.add_num(roul_id, num)
        self.ind_stats.add_num(roul_id, num)
        self.rules.proc_rules(roul_id)

    def add_nums(self, roul_id, nums):
        """Добавляет числа в статистику по одному"""
        for num in nums[::-1]:
            self.add_num(roul_id, num)

    def reload_roul(self, roul_id):
        """Очищает рулетку, а потом добавляет в неё числа из temp"""
        self.main_stats.reload_roul(roul_id)
        self.ind_stats.reload_roul(roul_id)
        self.rules.proc_rules(roul_id)

    def check_updates(self):
        """Проверяет есть ли обновления(изменения рулеток, юзеров или инд настроек) и применяет их"""
        self.main_stats.check_updates()
        self.ind_stats.check_updates()
