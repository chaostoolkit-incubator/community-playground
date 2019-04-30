import logging
import os
import os.path
from typing import Any, Dict

import cherrypy
from flask import Blueprint, current_app, Flask, jsonify, render_template, \
    request, session
from flask_caching import Cache
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
import opentracing
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from prometheus_flask_exporter import PrometheusMetrics
from requestlogger import ApacheFormatter, WSGILogger
import requests
from werkzeug.contrib.fixers import ProxyFix

__version__ = "0.1.0"

superpower = Blueprint("superpower", __name__)
cache = Cache()
metrics = PrometheusMetrics(app=None)

POWERSOURCE_URL = 'http://localhost:6061'
curdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
img_dir = os.path.normpath(os.path.join(curdir, "images"))
favicon_dir = os.path.normpath(os   .path.join(curdir, "public"))


def init_tracer():
    return Config(
        config={
            'logging': True,
            'local_agent': {
                'reporting_host': os.getenv("JAEGER_HOST", "localhost")
            },
            'sampler': {'type': 'const', 'param': 1}
        }, service_name='superpower', validate=True
    ).initialize_tracer()
tracer = FlaskTracer(init_tracer, True, app=superpower)


@superpower.route("/")
def index():
    with requests.Session() as req_session:
        parent_span = tracer.get_span(request)

        powerservice_url = current_app.config["POWERSOURCE_URL"]
        cid = session.get('cid')
        if cid is None:
            r = req_session.get(
                "{}/random".format(powerservice_url), timeout=(2, 2))
            cid = r.json()["character_id"]
            session['cid'] = cid

        headers = {
            "Connection": "close"
        }
        t = opentracing.tracer
        with t.start_span("fetch character", child_of=parent_span) as span:
            url = "{}/{}".format(powerservice_url, cid)
            span.set_tag('http.method', 'GET')
            span.set_tag('http.url', url)
            span.set_tag('span.kind', 'client')
            t.inject(span, opentracing.Format.HTTP_HEADERS, headers)
            info = req_session.get(url, headers=headers, timeout=(5, 2)).json()

        accept = request.headers.get('Accept')
        if accept == 'application/json':
            return jsonify(info)

        return render_template(
            "index.html", name=info["name"], description=info["description"],
            img_url=info["img_url"], learn_more_url=info["learn_more_url"])


@superpower.route("/health")
def health():
    return "", 200


@superpower.route("/live")
def live():
    return "", 200



def initialize_metrics(app: Flask):
    metrics.init_app(app)
    metrics.info('superpower', 'Application info', version=__version__)


def initialize_security_headers(app: Flask):
    csp = GOOGLE_CSP_POLICY.copy()
    csp["style-src"] = csp["style-src"].split(' ')
    csp["style-src"].append("'unsafe-inline'")

    csp["font-src"] = csp["font-src"].split(' ')
    csp["font-src"].append("'unsafe-inline'")

    csp["img-src"] = []
    csp["img-src"].append("'self'")
    Talisman(app, force_https=False, strict_transport_security=False,
        session_cookie_secure=False, content_security_policy=csp)


def initialize_cache(app: Flask):
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})


def mount_apps(app: Flask):
    app.wsgi_app = ProxyFix(app.wsgi_app)
    wsgiapp = WSGILogger(
        app.wsgi_app, [logging.StreamHandler()], ApacheFormatter(),
        propagate=False)
    cherrypy.tree.graft(wsgiapp, "/")

    cherrypy.tree.mount(None, "/favicon", {
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": favicon_dir,
            "tools.etags.on": True,
            "tools.etags.autotags": True
        }
    })

    cherrypy.tree.mount(None, "/public/images", {
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": img_dir,
            "tools.etags.on": True,
            "tools.etags.autotags": True
        }
    })


def get_powersource_service_url(default: str = POWERSOURCE_URL) -> str:
    return os.getenv("POWERSOURCE_URL", default)


def create_app(powersource_service: str) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(superpower)

    app.config["POWERSOURCE_URL"] = powersource_service
    app.secret_key = b'whatever'
    app.config["SECRET_KEY"] = app.secret_key

    initialize_security_headers(app)
    initialize_cache(app)
    initialize_metrics(app)
    mount_apps(app)
    return app

app = create_app(get_powersource_service_url())

