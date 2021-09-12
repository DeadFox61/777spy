from roulette.roulette_controller import RoulettesManager
from roulette.evo import EvoParser
from roulette.ezugi import EzugiParser
from parse_logger import configure_logger

configure_logger("roulette")

manager = RoulettesManager()
evo_parser = EvoParser()
ezugi_parser = EzugiParser()

manager.add_parser(evo_parser)
manager.add_parser(ezugi_parser)