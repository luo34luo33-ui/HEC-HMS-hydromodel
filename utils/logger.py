"""
日志记录模块
提供统一的日志记录接口
"""
import logging
import sys
from datetime import datetime
from typing import Optional


class Logger:
    """统一日志管理类"""

    _loggers = {}

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """获取或创建日志记录器"""
        if name in Logger._loggers:
            return Logger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 控制台输出
        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        Logger._loggers[name] = logger
        return logger

    @staticmethod
    def setup_file_handler(
        logger: logging.Logger,
        log_file: str,
        level: int = logging.DEBUG
    ):
        """添加文件日志处理器"""
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """获取日志记录器的便捷函数"""
    return Logger.get_logger(name)
