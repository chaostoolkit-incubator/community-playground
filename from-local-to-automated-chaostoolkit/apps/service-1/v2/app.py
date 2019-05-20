import time

from aioprometheus import render
import requests_async as requests
from starlette.applications import Starlette
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
import uvicorn

from metrics import configure_prometheus_metrics_exporter
from tracing import init_jaeger_tracer, incoming_trace, outgoing_trace


app = Starlette()
app.add_middleware(ServerErrorMiddleware)
tracer = init_jaeger_tracer()
configure_prometheus_metrics_exporter(app)


@app.route('/')
async def index(request: Request) -> JSONResponse:
    with incoming_trace("fetch-counter", request, tracer) as span:
        with outgoing_trace("next-count", request, tracer, span) as out:
            outgoing_span, ougoing_headers = out

            counter = await requests.get(
                'http://service2:8000/', headers=ougoing_headers, timeout=1)
            data = counter.json()

            count = data['last']
            app.counter_gauge.set({"path": request.url.path}, count)

            return JSONResponse({
                'svc': 'service1',
                'version': '2',
                'timestamp': time.time(),
                'count': count
            })


@app.route('/health')
async def health(request: Request) -> PlainTextResponse:
    return PlainTextResponse(content=b"")


@app.route("/metrics")
async def metrics(request: Request):
    content, http_headers = render(
        app.registry, [request.headers.get("accept", "application/json")])
    return PlainTextResponse(content, headers=http_headers)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
