class NoMatches(Exception):
    pass

class RoulettesManager():
    """Главный управляющий класс для чисел в рулетках"""
    def __init__(self):
        # В temp хранятся последние 500 чисел
        self.temp = {}
        self.load_data()
    def get_new(self, old,new,off=6):
        """Сравнивет и возвращает список новых чисел. Возбуждает NoMatches, если совпадений в old нет"""
        for i in range(len(new) - off+1):
            if old[:off] == new[i:i+off]:
                return new[:i]
        raise NoMatches("Нет совпадений в old")

    def load_data(self):
        """Загружает данные, хранящиеся в бд"""
        pass
    def proc_numbers(self, roul_id, nums):
        """Обрабатывает числа nums рулетки roul_id. """
