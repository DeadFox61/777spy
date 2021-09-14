import threading
from loguru import logger
import time

from db import db_roulette as db
from roulette.main_stats import RoulsStats
from roulette.personal_stats import IndRoulStats

class NoMatches(Exception):
    pass
class NotEnoughNums(Exception):
    pass
class NoSuchRoulette(Exception):
    pass



class RoulettesManager():
    """Главный управляющий класс для чисел в рулетках"""
    MIN_NUM_COUNT = 6
    def __init__(self):
        # В temp хранятся последние 500 чисел
        self.temp = {}
        self.lock = threading.Lock()
        self.stats = RoulsStats()
        self.ind_stats = IndRoulStats(self)
        self.load_data()
    def get_new(self, old, new):
        """Сравнивет и возвращает список новых чисел. Возбуждает NoMatches, если совпадений в old нет"""
        off = self.MIN_NUM_COUNT
        if len(new) < off:
            raise NotEnoughNums("Not enough nums")
        for i in range(len(new) - off+1):
            if old[:off] == new[i:i+off]:
                return new[:i]

        logger.error(f'{new} не найден в {old}')
        raise NoMatches("Нет совпадений в old")

    def load_data(self):
        """Загружает данные, хранящиеся в бд"""
        logger.info("Loading data from db..")
        self.temp = db.get_init_data()
        self.stats.init_rouls(self.temp)
        self.ind_stats.load_data()
        logger.info("Data loaded")

    def add_numbers(self, roul_id, nums):
        """Добавляет числа в рулетку"""
        db.add_numbers(roul_id, nums)
        self.temp[roul_id]['nums'] = nums+self.temp[roul_id]['nums']
        for num in nums[::-1]:
            self.stats.add(roul_id, num)
        try:
            self.ind_stats.add_nums(roul_id, nums)
        except Exception as e:
            logger.error(e)
        logger.info(f'В ({roul_id}){self.temp[roul_id]["name"]} добавлены {nums}')

    def reload_roul(self, roul_id, nums):
        """Очищает все числа рулетки и добавляет nums"""
        db.clear_roul(roul_id)
        db.add_numbers(roul_id, nums)
        self.temp[roul_id]['nums'] = nums
        self.stats.reload_roul(roul_id, self.temp[roul_id]["name"], nums)
        logger.info(f'({roul_id}){self.temp[roul_id]["name"]} очищена')
    def get_nums(self, roul_id):
        """Возвращает числа рулетки roul_id"""
        if roul_id in self.temp:
            return self.temp[roul_id]['nums']
        else:
            raise NoSuchRoulette(f"Рулетка с id {roul_id} не инициализирована")
    def proc_numbers(self, roul_id, nums):
        """Обрабатывает числа nums рулетки roul_id. Парсеры вызывают эту функцию, когда получают числа"""
        with self.lock:
            try:
                current = self.get_nums(roul_id)
                new = self.get_new(current,nums)
                if new:
                    self.add_numbers(roul_id, new)
            except NoMatches:
                self.reload_roul(roul_id, nums)
            except NotEnoughNums:
                pass
            except NoSuchRoulette as e:
                logger.error(e)
    def add_parser(self, parser):
        parse_thread = threading.Thread(target=parser.start_parsing, args=(self.proc_numbers,))
        parse_thread.start()