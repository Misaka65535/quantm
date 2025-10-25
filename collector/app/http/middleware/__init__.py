from fastapi import FastAPI
from .request_id_middleware import RequestIdMiddleware
from config.config import DevelopmentSettings, ProductionSettings, get_settings


def register(server: FastAPI, settings: DevelopmentSettings | ProductionSettings):
    # 注册中间件
    server.add_middleware(RequestIdMiddleware)
