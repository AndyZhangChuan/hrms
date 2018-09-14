from core import app

from flask_cors import CORS
CORS(app, supports_credentials=True)


@app.route('/health')
def fortune_healthcheck():
    return "ok"
