from contextvars import ContextVar
from config.config import DevelopmentSettings, ProductionSettings, get_settings

import uuid

settings = get_settings()
# 使用任务request_id来实现全链路日志追踪
_x_request_id: ContextVar[str] = ContextVar('x_request_id', default="")  # 请求ID
REQUEST_ID_KEY = "X-Request-Id"


class TraceID:
    """全链路追踪ID"""
    _x_request_id: ContextVar[str] = ContextVar('x_request_id', default="")  # 请求ID

    @staticmethod
    def set(req_id: str) -> ContextVar[str]:
        """设置请求ID，外部需要的时候，可以调用该方法设置
        Returns:
            ContextVar[str]: _description_
        """
        if not req_id:
            req_id = uuid.uuid5(uuid.uuid1(uuid.getnode(), 1), settings.NAME).hex
        _x_request_id.set(req_id)
        return _x_request_id
