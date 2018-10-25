import json
import traceback

from flask import render_template, request, jsonify

from controller.decorater import get_request_proj_id, get_request_org_id
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
        proj_id = get_request_proj_id()
        org_id = get_request_org_id()
        options = json.loads(request.args.get('options'))
        filters = json.loads(request.args.get('filters'))
        if 'proj_id' not in filters:
            filters['proj_id'] = proj_id
        if 'org_id' not in filters:
            filters['org_id'] = org_id
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