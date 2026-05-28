from loguru import logger

logger.add(
    "logs/framework.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO"
)
