# core/logger.py
import logging
from logging.handlers import RotatingFileHandler
from core.config import settings

def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    if not logger.handlers:
        # 콘솔 출력
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ))
        logger.addHandler(console_handler)

        # 파일 출력 (5MB씩 3개까지 순환)
        file_handler = RotatingFileHandler(
            settings.LOG_FILE, maxBytes=5*1024*1024, backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ))
        logger.addHandler(file_handler)

    return logger

# 전역 로거
logger = get_logger()
