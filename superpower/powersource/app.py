import logging
import os
import os.path
import random

import cherrypy
import click
from flask import abort, Blueprint, Flask, jsonify
from flask_caching import Cache
from requestlogger import ApacheFormatter, WSGILogger
import opentracing
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from prometheus_flask_exporter import PrometheusMetrics
import simplejson as json
import slugify
from werkzeug.contrib.fixers import ProxyFix

__version__ = "0.1.0"
THUMBNAIL_NOT_FOUND = 'http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available'

powersource = Blueprint("powersource", __name__)
cache = Cache()
metrics = PrometheusMetrics(app=None)

curdir = os.getcwd()
characters = []
indexes = []


def init_tracer():
    return Config(
        config={
            'logging': True,
            'local_agent': {
                'reporting_host': os.getenv("JAEGER_HOST", "localhost")
            },
            'sampler': {'type': 'const', 'param': 1}
        }, service_name='powersource', validate=True
    ).initialize_tracer()
tracer = FlaskTracer(init_tracer, True, app=powersource)


def load_characters():
    with open(os.path.join(curdir, "characters.json")) as f:
        characters.extend(json.load(f))
        for index, c in enumerate(characters):
            thumbnail = c["thumbnail"]
            if thumbnail["path"] == THUMBNAIL_NOT_FOUND:
                continue
            indexes.append(index)


@powersource.route("/<int:character_id>")
@cache.cached(timeout=600)
def index(character_id: int):
    if character_id not in indexes:
        return abort(404)

    character = characters[character_id]
    extension = character["thumbnail"]["extension"]
    img_url = "{}.{}".format(
        slugify.slugify(character["name"]),
        extension
    )
    learn_more_url = None
    for url in character.get("urls", []):
        if url["type"] == "detail":
            learn_more_url = url["url"]
            break

    return jsonify(dict(
        name=character["name"], description=character["description"],
        img_url=img_url, learn_more_url=learn_more_url))


@powersource.route("/random")
def rand() -> str:
    return jsonify({"character_id": random.choice(indexes)})


@powersource.route("/health")
def health():
    return "", 200


@powersource.route("/live")
def live():
    return "", 200



def initialize_metrics(app: Flask):
    metrics.init_app(app)
    metrics.info('powersource', 'Application info', version=__version__)


def initialize_cache(app: Flask):
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})


def mount_apps(app: Flask):
    app.register_blueprint(powersource)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    wsgiapp = WSGILogger(
        app.wsgi_app, [logging.StreamHandler()], ApacheFormatter(),
        propagate=False)
    cherrypy.tree.graft(wsgiapp, "/")



def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(powersource)
    load_characters()
    initialize_cache(app)
    initialize_metrics(app)
    mount_apps(app)
    return app

app = create_app()