"""Middleware to log request time."""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("uvicorn")


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request time."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request time.

        Args:
            request: Request object
            call_next: Next call to make

        Returns:
            Response object
        """
        start_time = time.perf_counter()

        response = await call_next(request)

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        log.debug(f"{request.method} {request.url.path} took {time_taken:.4f} seconds")

        return response
