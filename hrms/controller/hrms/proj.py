# -*- encoding: utf8 -*-

from core import app
from flask import jsonify
from hrms.forms.hrms.proj import ProjUpdateForm
from hrms.service.hrms import proj_service
from hrms.dao.manager.hrms.proj import ProjMgr


@app.route("/test")
def test_proj():
    """
    测试项目开始
    :return:
    """
    proj = ProjMgr.get(1)
    return jsonify(status='ok', proj_name=proj.proj_name)


@app.route("/proj", methods=['POST'])
def create_proj():
    """
    创建项目
    :return:
    """
    form = ProjUpdateForm()
    if not form.validate_on_submit():
        return jsonify(status='error', msg=form.errors)
    pass


@app.route("/proj", methods=['PUT'])
def update_proj():
    """
    更改项目
    :return:
    """
    pass


@app.route("/proj/<int:proj_id>", methods=['DELETE'])
def delete_proj(proj_id):
    pass


@app.route("/proj", methods=['GET'])
def get_proj_list():
    pass


