import abc

class RouletteParser():
	"""Основной класс парсинга рулетки"""

	@abc.abstractmethod
	def start_parsing(self, on_parse):
		"""Основная функция парсинга. Должна передавать спаршенные данные в функцию on_parse"""
		return