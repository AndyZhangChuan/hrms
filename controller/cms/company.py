# -*- encoding: utf8 -*-

from core import app
from flask import jsonify
from flask import request
from service import company_service, proj_service


@app.route("/company", methods=['GET'])
def get_company_list():
    try:
        data = company_service.get_company_list(int(request.args.get("page")))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/plugins", methods=['GET'])
def get_proj_plugins_by_company():
    try:
        data = proj_service.get_proj_plugins_by_company(int(request.args.get("page")), int(request.args.get("company_id")))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/plugin/update", methods=['POST', 'GET'])
def update_plugin_maps():
    try:
        params = {
            'proj_id': request.form.get('proj_id', 0),
            'plugin_id': request.form.get('plugin_id', 0),
            'plugin_name': request.form.get('plugin_name', ''),
            'props': request.form.get('props', ''),
            'is_del': int(request.form.get('is_del', 0)),
        }

        plugins = proj_service.update_proj_plugin(params)
        return jsonify(status='ok', content=plugins)
    except Exception, ex:
        return jsonify(status='error', message=ex.message)
