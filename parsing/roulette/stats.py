from roulette.main_stats import RoulsStats
from roulette.personal_stats import IndRoulStats



class AllStats(object):
    """Класс управления статистикой"""
    def __init__(self):
        self.main_stats = RoulsStats()
        self.ind_stats = IndRoulStats()

    def add_nums(self, roul_id, nums):
        """Добавляет числа в статистику"""