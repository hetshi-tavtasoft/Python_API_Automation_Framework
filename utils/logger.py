import sys
from loguru import logger

# Clear default handler
logger.remove()

# Format with process and thread identifiers for xdist parallel runs
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>P:{process}</cyan>:<cyan>T:{thread}</cyan> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Console logger
logger.add(
    sys.stdout,
    format=log_format,
    level="INFO",
    colorize=True
)

# Main log file
logger.add(
    "logs/framework.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | P:{process}:T:{thread} | {name}:{function}:{line} - {message}",
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    encoding="utf-8"
)

# Errors only log file
logger.add(
    "logs/errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | P:{process}:T:{thread} | {name}:{function}:{line} - {message}",
    rotation="5 MB",
    retention="10 days",
    level="WARNING",
    encoding="utf-8"
)
