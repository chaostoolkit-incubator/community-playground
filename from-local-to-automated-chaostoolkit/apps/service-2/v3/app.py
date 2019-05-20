import asyncio
import itertools

from aioprometheus import render
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
import uvicorn

from metrics import configure_prometheus_metrics_exporter
from tracing import init_jaeger_tracer, incoming_trace


app = Starlette()
counter = itertools.count(0, 1)
tracer = init_jaeger_tracer()
configure_prometheus_metrics_exporter(app)


@app.route('/')
async def index(request: Request) -> JSONResponse:
    with incoming_trace("next-count", request, tracer) as span:
        return JSONResponse({
            'svc': 'service2',
            'version': '3',
            'last': next(counter)
        })


@app.route('/health')
async def health(request: Request) -> PlainTextResponse:
    return PlainTextResponse(content=b"", status_code=500)


@app.route("/metrics")
async def metrics(request: Request):
    content, http_headers = render(
        app.registry, [request.headers.get("accept", "application/json")])
    return PlainTextResponse(content, headers=http_headers)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
