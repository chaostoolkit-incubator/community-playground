import contextlib
from typing import Any, Dict, Generator

from jaeger_client import Config
from opentracing import child_of, Span, tags, Tracer
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from opentracing.propagation import Format
from starlette.requests import Request


__all__ = ["init_jaeger_tracer", "incoming_trace"]


def init_jaeger_tracer() -> Tracer:
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'propagation': "b3",
            'local_agent': {
                'reporting_host': 'localhost'
            }
        },
        service_name='service2',
        validate=True,
        scope_manager=AsyncioScopeManager()
    )
    return config.initialize_tracer()


@contextlib.contextmanager
def incoming_trace(operation: str, request: Request,
                   tracer: Tracer) -> Generator[Span, None, None]:
    span_context = tracer.extract(
        format=Format.HTTP_HEADERS,carrier=dict(request.headers))

    params = {}
    if span_context:
        params["child_of"] = span_context
    with tracer.start_span(operation, **params) as span:
        span.set_tag('http.url', request.url)

        remote_ip = request.client.host
        if remote_ip:
            span.set_tag(tags.PEER_HOST_IPV4, remote_ip)

        remote_port = request.client.port
        if remote_port:
            span.set_tag(tags.PEER_PORT, remote_port)

        yield span
