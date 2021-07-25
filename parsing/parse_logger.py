from loguru import logger

def get_logger():
	logger.add("logs/parse.log", format="{time} {level} {message}", rotation="100 MB", compression = "zip", backtrace=True, diagnose=True) 
	return logger