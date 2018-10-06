from flask import render_template

from core import app

import hrms
import cms


@app.route('/health')
def fortune_healthcheck():
    return "ok"


@app.route('/h5')
def page_h5():
    return render_template('h5.html')
