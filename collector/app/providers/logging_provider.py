import logging
from sys import stdout

from fastapi import FastAPI, Request
from loguru import logger
from contextvars import ContextVar, Context
from starlette.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from config.config import DevelopmentSettings, ProductionSettings, get_settings
from app.providers.traceid_provider import TraceID, REQUEST_ID_KEY, _x_request_id


def _logger_filter(record):
    record['request_id'] = f"{_x_request_id.get()}"
    return record['request_id']


class InterceptHandler(logging.Handler):
    """拦截 fastapi 主程序的 log

    Args:
        logging (_type_): _description_
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def register(app: FastAPI, settings: DevelopmentSettings | ProductionSettings):
    """logger 设置.

    在 debug 模式下会拦截所有包括主程序的 log.
    ERROR 会专门存放在 LOG_PATH_ERROR 中.
    """

    level = settings.LOG_LEVEL
    # path = settings.LOG_PATH
    rotation = settings.LOG_ROTATION
    retention = settings.LOG_RETENTION

    if not settings.DEBUG:  # 如果不是 debug 模式, 则不拦截主程序的 log
        # intercept everything at the root logger
        logging.root.handlers = [InterceptHandler()]
        logging.root.setLevel(level)

        # remove every other logger's handlers and propagate to root logger
        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

    # configure loguru
    try:
        # logger.configure(extra={"request_id": ''})  # Default values 否则会报错
        logger.remove(0)  # 移除默认设置
    except Exception:
        pass

    log_format = (
        # 时间信息 + UUID
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {request_id} | "
        # 日志级别，居中对齐
        "<level>{level: ^8}</level> | "
        # 进程和线程信息
        "process [<cyan>{process}</cyan>]:<cyan>{thread}</cyan> | "
        # 文件、函数和行号
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        # 日志消息
        "<level>{message}</level>"
    )
    logger.level("DEBUG", color="<cyan>")
    logger.level("INFO", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.configure(
        handlers=[
            {
                "sink": stdout,
                "enqueue": True,  # 异步
                "format": log_format,
                "level": level,
                "colorize": True,  # 启用彩色输出
                "filter": _logger_filter,
            },
            {
                "sink": settings.LOG_PATH,
                "enqueue": True,  # 异步
                "format": log_format,
                "level": level,
                "rotation": rotation,
                "retention": retention,
                "compression": "tar.xz",
                "filter": _logger_filter,
            },
            {
                "sink": settings.LOG_PATH_ERROR,
                "enqueue": True,  # 异步
                "format": log_format,
                "level": settings.LOG_LEVEL_ERROR,
                "rotation": rotation,
                "retention": retention,
                "compression": "tar.xz",
                "filter": _logger_filter,
            },
        ]
    )
