from loguru import logger
from fastapi import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.providers.traceid_provider import TraceID, REQUEST_ID_KEY
from app.models.response_model import server_error


class RequestIdMiddleware(BaseHTTPMiddleware):
    """ 全链路追踪ID记录中间件"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        1.设置日志的全链路追踪
        2.记录错误日志
        """
        try:
            _req_id_val = request.headers.get(REQUEST_ID_KEY, "")
            req_id = TraceID.set(_req_id_val)
            logger.info(f"request: {request.method} {request.url}")
            response = await call_next(request)
            response.headers[REQUEST_ID_KEY] = req_id.get()
            logger.info(f"response: {request.method} {request.url} {response.status_code}")
            req_id.set(None)
            return response
        except Exception as ex:
            logger.exception(ex)  # 这个方法能记录错误栈
            return server_error(status_code=500)
        finally:
            pass
