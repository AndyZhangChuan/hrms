# -*- encoding: utf8 -*-

from core import app
from hrms import proj
from cms import company
from ..plugins import view

from flask_cors import CORS
CORS(app, supports_credentials=True)

@app.route('/health')
def fortune_healthcheck():
    return "ok"

