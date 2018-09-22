from core import app

import hrms
import cms


@app.route('/health')
def fortune_healthcheck():
    return "ok"
