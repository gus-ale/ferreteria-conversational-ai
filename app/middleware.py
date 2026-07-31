import time
from uuid import uuid4

from fastapi import Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

REQUESTS = Counter(
    "ferrebot_http_requests_total",
    "HTTP requests handled by FerreBot",
    ["method", "path", "status"],
)
LATENCY = Histogram(
    "ferrebot_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request.state.request_id = request_id
        started = time.perf_counter()

        response = await call_next(request)
        elapsed = time.perf_counter() - started
        path = request.url.path
        REQUESTS.labels(request.method, path, response.status_code).inc()
        LATENCY.labels(request.method, path).observe(elapsed)
        response.headers["X-Request-ID"] = request_id
        return response
