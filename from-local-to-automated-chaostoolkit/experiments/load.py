import asyncio
import threading
import time

from chaoslib.types import Configuration, Secrets
from logzero import logger
import opentracing
import requests as requests

__all__ = ['single']


def single(url: str, duration: int, frequency: float = 1.0,
           configuration: Configuration = None, secrets: Secrets = None):
    """
    Run a loop for up to the given duration in a thread and call the remote
    service following the given frequency (in seconds).

    Send traces along the way to OpenTracing.
    """
    end = time.time() + duration
    tracer = opentracing.global_tracer()
    scope = tracer.scope_manager.active
    parent = scope.span

    def f():
        logger.info("Calling '{}' for {}s every {}s".format(
            url, duration, frequency
        ))
        while True:
            headers = {}

            with tracer.start_span("call-service1", child_of=parent) as span:
                span.set_tag('http.method','GET')
                span.set_tag('http.url', url)
                span.set_tag('span.kind', 'client')
                span.tracer.inject(span, 'http_headers', headers)

                try:
                    r = requests.get(url, headers=headers, timeout=1)
                    if r.status_code == 200:
                        logger.debug("Response from service: {}".format(
                            r.json()))
                    else:
                        logger.debug("Failed to get response from server")
                    span.set_tag('http.status_code', r.status_code)
                except Exception:
                    logger.debug(
                        "Failed to talk to '{}'".format(url), exc_info=True)

            if time.time() > end:
                return

            time.sleep(frequency)

    loop = threading.Thread(target=f)
    loop.start()
