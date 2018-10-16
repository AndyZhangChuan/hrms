import json
import traceback

from flask import render_template, request, jsonify

from core import app

import hrms
import cms
import capp
import framework
from data import dao


@app.route('/health')
def fortune_healthcheck():
    return "ok"


@app.route('/h5')
def page_h5():
    return render_template('h5.html')


@app.route("/data/query", methods=['GET'])
def data_query():
    try:
        options = json.loads(request.args.get('options'))
        filters = json.loads(request.args.get('filters'))
        query = options['query']
        result = ''
        if query.startswith('get'):
            result = dao.get(options['module'], query, options['attrs'], filters)
        if query.startswith('list'):
            result = dao.list(options['module'], query, options['attrs'], filters)
        return jsonify(status='ok', data=result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)