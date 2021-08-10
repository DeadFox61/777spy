from loguru import logger

# Настраивает логгер
def configure_logger(filename = "default"):
	logger.add(f"logs/parse_{filename}.log", format="{time} {level} {message}", rotation="10 MB", compression = "zip", backtrace=True, diagnose=True)