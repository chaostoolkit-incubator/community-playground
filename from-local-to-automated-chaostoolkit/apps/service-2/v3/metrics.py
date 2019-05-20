import socket

from aioprometheus import Counter, Gauge, Registry
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIInstance

__all__ = ["configure_prometheus_metrics_exporter"]


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, errormiddleware, webapp: Starlette):
        BaseHTTPMiddleware.__init__(self, errormiddleware)
        self.webapp = webapp

    async def dispatch(self, request: Request, call_next) -> ASGIInstance:
        method = request.method
        path = request.url.path

        if path in ["/metrics", "/health"]:
            return await call_next(request)

        self.webapp.svc_requests_total.inc({"path": path, "method": method})
        try:
            response = await call_next(request)
        except Exception as e:
            self.webapp.svc_internal_error_total.inc({
                "path": path, "method": method, "type": str(type(e))
            })
            raise
            
        self.webapp.svc_responses_total.inc({
            "path": path, "method": method,
            "status_code": response.status_code
        })

        return response


def configure_prometheus_metrics_exporter(app: Starlette):
    app.add_middleware(MetricsMiddleware, webapp=app)

    app.registry = Registry()

    const_labels = {
        "host": socket.gethostname(),
        "name": "service2",
        "version": "3"
    }

    app.counter_gauge = Gauge(
        "counter", "Current count.", const_labels=const_labels)
    app.registry.register(app.counter_gauge)

    app.svc_requests_total = Counter(
        "svc_requests_total", "Count of service HTTP requests",
        const_labels=const_labels)
    app.registry.register(app.svc_requests_total)

    app.svc_responses_total = Counter(
        "svc_responses_total", "Count of service HTTP responses",
        const_labels=const_labels)
    app.registry.register(app.svc_responses_total)

    app.svc_internal_error_total = Counter(
        "svc_internal_error_total",
        "Histogram of internal errors by method, path and type of error",
        const_labels=const_labels)
    app.registry.register(app.svc_internal_error_total)
