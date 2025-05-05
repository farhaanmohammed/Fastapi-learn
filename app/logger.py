from loguru import logger
import sys
import os

# Make sure logs/ directory exists
os.makedirs("logs", exist_ok=True)

logger.remove()  # Remove default Loguru handler


logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO",
    enqueue=True,  # Good for async frameworks like FastAPI
    backtrace=True,
    diagnose=True,
)

# Optional: Log to file as well
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
    backtrace=True,
    diagnose=True,
)