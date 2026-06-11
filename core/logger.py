import sys
from loguru import logger

logger.remove()

_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>P:{process}</cyan>:<cyan>T:{thread}</cyan> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

_FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | P:{process}:T:{thread} | {name}:{function}:{line} - {message}"

logger.add(sys.stdout, format=_FORMAT, level="INFO", colorize=True)
logger.add("logs/framework.log", format=_FILE_FORMAT, rotation="5 MB", retention="10 days", level="INFO", encoding="utf-8")
logger.add("logs/errors.log", format=_FILE_FORMAT, rotation="5 MB", retention="10 days", level="WARNING", encoding="utf-8")
