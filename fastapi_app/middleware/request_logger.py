import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("request_logger")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000  # ms

        logger.info(
            "%s %s | status=%s | duration=%.2f ms | ip=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
            request.client.host,
        )

        return response
