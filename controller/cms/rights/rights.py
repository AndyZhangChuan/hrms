# -*- encoding: utf8 -*-

import sys
from flask import jsonify, request
from core import app
from controller.decorater.rights import rights
from service.rights import rights_resource_service
from commons.constants import RightsResourceConstant
from controller.forms.rights import RightsResourceAddForm, RightsResourceUpdateForm
reload(sys)
sys.setdefaultencoding('utf8')


@app.route("/rights", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_ADD)
def add_rights_resource():
    form = RightsResourceAddForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_resource_service.add_rights_resource(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights", methods=['PUT'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_UPDATE)
def update_rights_resource():
    form = RightsResourceUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_resource_service.update_rights_resource(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/<int:resource_id>", methods=['DELETE'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_DELETE)
def delete_rights_resource(resource_id):
    try:
        data = rights_resource_service.delete_rights_resource(resource_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_LIST)
def get_rights_resource_list():
    try:
        data = rights_resource_service.get_rights_resource_list(int(request.args.get("page", 1)))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/<int:resource_id>", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_DETAIL)
def get_rights_resource_detail(resource_id):
    try:
        data = rights_resource_service.get_rights_resource_detail(resource_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/editable/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_LIST)
def get_rights_editable_list():
    try:
        data = rights_resource_service.get_rights_tree()
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/uiElements/byParentId", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_LOGIN)
def get_rights_resource_list_by_parent_id():
    try:
        data = rights_resource_service.get_rights_resource_list_by_parent_id(int(request.args.get("parent_id", 1)))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


