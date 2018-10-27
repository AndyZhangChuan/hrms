# -*- encoding: utf8 -*-
import traceback

from core import app
from flask import jsonify
from flask import request
from service import org_service
from service.framework import plugin_service


@app.route("/org", methods=['GET'])
def get_org_list():
    try:
        data = org_service.get_org_list()
        return jsonify(status='ok', data=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/plugins", methods=['GET'])
def get_proj_plugins_by_org():
    try:
        data = plugin_service.get_plugins(int(request.args.get("page", 1)), int(request.args.get("org_id", 0)))
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/plugin", methods=['POST'])
def update_plugin_maps():
    try:
        plugins = plugin_service.update_proj_plugin(request.form)
        return jsonify(status='ok', content=plugins)
    except Exception, ex:
        return jsonify(status='error', message=ex.message)
