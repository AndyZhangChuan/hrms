# -*- encoding: utf8 -*-

import sys
from flask import jsonify, request
from core import app
from controller.decorater.rights import rights
from commons.constants import RightsResourceConstant
from service.rights import rights_role_service
from controller.forms.rights import RightsRoleAddForm, RightsRoleUpdateForm, RightsRoleResourceAllocateForm

reload(sys)
sys.setdefaultencoding('utf8')


@app.route("/rights/role", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_ROLE_ADD)
def add_rights_role():
    form = RightsRoleAddForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_role_service.add_rights_role(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/role", methods=['PUT'])
@rights(RightsResourceConstant.RIGHTS_ROLE_UPDATE)
def update_rights_role():
    form = RightsRoleUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_role_service.update_rights_role(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/role/<int:role_id>", methods=['DELETE'])
@rights(RightsResourceConstant.RIGHTS_ROLE_DELETE)
def delete_rights_role(role_id):
    try:
        data = rights_role_service.delete_rights_role(role_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/role/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_ROLE_LIST)
def get_rights_role_list():
    try:
        data = rights_role_service.get_rights_role_list(int(request.args.get("page", 1)))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/role/<int:role_id>", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_ROLE_DETAIL)
def get_rights_role_detail(role_id):
    try:
        data = rights_role_service.get_rights_role_detail(role_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/rights/role/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_ROLE_UPDATE)
def allocate_rights_role():
    form = RightsRoleResourceAllocateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        rights_ids = [int(item) for item in form.rights_ids.data.split(",")]
        data = rights_role_service.rights_role_resource_allocate(form.role_id.data, rights_ids)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)
