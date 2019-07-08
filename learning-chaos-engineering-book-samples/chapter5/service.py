# -*- coding: utf-8 -*-
from datetime import datetime
import io
import time
import threading
from wsgiref.validate import validator
from wsgiref.simple_server import make_server

EXCHANGE_FILE = "./exchange.dat"


def update_exchange_file():
    """
    Writes the current date and time every 10 seconds into the exchange file.

    The file is created if it does not exist.
    """
    print("Will update to exchange file")
    while True:
        with io.open(EXCHANGE_FILE, "w") as f:
            f.write(datetime.now().isoformat())
        time.sleep(10)


def simple_app(environ, start_response):
    """
    Read the content of the exchange file and return it.
    """
    start_response('200 OK', [('Content-type', 'text/plain')])
    with io.open(EXCHANGE_FILE) as f:
        return [f.read().encode('utf-8')]


if __name__ == '__main__':
    t = threading.Thread(target=update_exchange_file)
    t.start()

    httpd = make_server('', 8080, simple_app)
    print("Listening on port 8080....")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        t.join(timeout=1)