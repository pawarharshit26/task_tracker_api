import time
import uuid

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import request_id_ctx

log = structlog.get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        log.info(
            "request_started",
            request_id=request.state.request_id,
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
        )

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        log.info(
            "request_completed",
            request_id=request.state.request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time, 2),
        )

        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        request_id_ctx.set(request_id)  # <-- set context variable
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
