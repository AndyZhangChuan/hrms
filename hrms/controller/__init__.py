# -*- encoding: utf8 -*-


from core import app
from hrms import proj


@app.route('/health')
def fortune_healthcheck():
    return "ok"

