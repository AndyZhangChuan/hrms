# -*- encoding: utf8 -*-

import logging
import sys

import requests
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flaskext.uploads import UploadSet, configure_uploads

from configs import config
from core.db.router import AutoRouteSQLAlchemy
from core.dapper.intercept import XB3HTTPAdapter
from core.log import getLogger
reload(sys)
sys.setdefaultencoding('utf8')
log = getLogger("hrms")


def create_app():
    flask_app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER, static_folder=config.STATIC_FOLDER)
    flask_app.config.from_object(config)
    flask_app.template_folder = flask_app.config['TEMPLATE_FOLDER']
    flask_app.static_folder = flask_app.config['STATIC_FOLDER']
    log.info("create app done")

    return flask_app


def get_app_name():
    return app.config.get('__APP_NAME__', '0')


def create_http_pool():
    pool = requests.Session()
    pool.mount('http://', XB3HTTPAdapter())
    pool.mount('https://', XB3HTTPAdapter())
    log.info("create http_pool done")
    return pool


def config_file_uploads():
    uploads = UploadSet("images", ("txt, jpg, png"))
    configure_uploads(app, uploads)
    log.info("config file_uploads done")


def init_file_handler():
    # create file handler which logs even debug messages
    fh = logging.FileHandler(app.config['HRMS_DEBUG_LOG'])
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s-%(name)s-%(levelname)s-%(process)d-%(processName)s-%(funcName)s %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.info("init file_handler done")


# init app
app = create_app()

# init db
db = AutoRouteSQLAlchemy(app)

# init http_pool
http_pool = create_http_pool()

# init toolbar
toolbar = DebugToolbarExtension(app)

# configure file uploads
config_file_uploads()

# init file handler
init_file_handler()


from inspect import getmembers, isclass
import plugins

plugin_pool = {}
members = getmembers(plugins)
for member in members:
    if isclass(member[1]):
        plugin_pool[member[0]] = member[1]


log.info("project init done")
