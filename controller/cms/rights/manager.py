# -*- encoding: utf8 -*-

import sys
from flask import jsonify, request
from core import app
from controller.decorater.rights import rights
from commons.constants import RightsResourceConstant
from service.rights import rights_user_service
from controller.forms.rights import ManagerAddForm, ManagerRoleAllocateForm, ManagerUpdateForm,\
    ManagerLoginForm, ManagerProjAllocateForm

reload(sys)
sys.setdefaultencoding('utf8')


@rights(RightsResourceConstant.RIGHTS_MANAGER_ADD)
@app.route("/manager", methods=['POST'])
def add_manager():
    form = ManagerAddForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_user_service.add_manager(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@rights(RightsResourceConstant.RIGHTS_MANAGER_UPDATE)
@app.route("/manager", methods=['PUT'])
def update_manager():
    form = ManagerUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_user_service.update_manager(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@rights(RightsResourceConstant.RIGHTS_MANAGER_DETAIL)
@app.route("/manager/<int:manager_id>", methods=['GET'])
def get_manager_detail(manager_id):
    try:
        data = rights_user_service.get_manager_detail(manager_id)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@rights(RightsResourceConstant.RIGHTS_MANAGER_LIST)
@app.route("/manager", methods=['GET'])
def get_manager_list():
    try:
        data = rights_user_service.get_manager_list(int(request.args.get("page", 1)))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/manager/login", methods=['POST'])
def manager_login():
    form = ManagerLoginForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_user_service.manager_login(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/manager/role/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_ROLE_ALLOCATE)
def allocate_manager_role():
    form = ManagerRoleAllocateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        role_list = form.role_ids.data.split(",")
        role_ids = [int(role_id) for role_id in role_list]
        data = rights_user_service.manager_role_allocate(form.manager_id.data, role_ids)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/manager/proj/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_PROJ_ALLOCATE)
def allocate_manager_proj():
    form = ManagerProjAllocateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    try:
        data = rights_user_service.manager_proj_rights_allocate(form)
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/manager/login/code/send", methods=['POST'])
def login_code_send():
    """
    发送微信登陆验证码
    :return:
    """
    try:
        phone = int(request.form.get("phone"))
        data = rights_user_service.send_login_auth_code(phone)
        return jsonify(data)
    except Exception, ex:
        print ex
        return jsonify(status="fail", msg="短信验证码发送失败!")
