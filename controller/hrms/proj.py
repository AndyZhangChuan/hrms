# -*- encoding: utf8 -*-

from core import app
from flask import jsonify
from flask import request
from controller.forms import ProjUpdateForm, ProjStatusChangeForm
from service import proj_service
from commons.utils import web_util


@app.route("/proj", methods=['POST'])
def create_proj():
    """
    创建项目
    :return:
    """
    form = ProjUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = proj_service.create_proj(web_util.get_operator_id(), form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj", methods=['PUT'])
def update_proj():
    """
    更改项目
    :return:
    """
    form = ProjUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = proj_service.update_proj(web_util.get_operator_id(), form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/<int:proj_id>", methods=['DELETE'])
def delete_proj(proj_id):
    try:
        data = proj_service.delete_proj(web_util.get_operator_id(), proj_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj", methods=['GET'])
def get_proj_list():
    try:
        data = proj_service.get_proj_list(int(request.args.get("page")))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/status", methods=['PUT'])
def update_proj_status():
    """
    更新项目状态
    :return:
    """
    form = ProjStatusChangeForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = proj_service.change_proj_status(web_util.get_operator_id(), form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)
