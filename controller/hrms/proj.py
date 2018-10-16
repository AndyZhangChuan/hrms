# -*- encoding: utf8 -*-
import time
import traceback

from werkzeug.utils import secure_filename

from core import app
from flask import jsonify
from flask import request
from controller.forms.proj import ProjUpdateForm, ProjStatusChangeForm
from data import dao
from service import proj_service
from commons.utils import web_util, time_util


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
        data = proj_service.get_proj_list(int(request.args.get("company_id")), int(request.args.get("page")))
        return jsonify(data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/base", methods=['GET'])
def get_proj_base():
    try:
        getter = 'get_proj_by_id'
        attrs = ['logo_url', 'intro_list_pics', 'update_time_str']
        base = dao.get('proj', getter, attrs, {'proj_id': 1})
        return jsonify(status='ok', content=base)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/content", methods=['GET'])
def get_proj_content():
    try:
        proj_id = int(request.args.get("proj_id"))
        detail = proj_service.get_proj_detail(proj_id)
        highlight = proj_service.get_proj_highlight(proj_id)
        return jsonify(status='ok', highlight=highlight, detail=detail)
    except Exception, ex:
        traceback.print_exc()
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


@app.route("/proj/richtext", methods=['POST'])
def create_proj_richtext():
    try:
        form = request.form
        result = proj_service.create_or_update_proj_rich_text(form['proj_id'], form['title'], form['text_type'], form['rich_text'], int(form.get('sequence', 0)), form.get('subtitle', ''), int(form.get('rich_text_id', 0)))
        return jsonify(status='ok', content=result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/richtext", methods=['DELETE'])
def delete_proj_richtext():
    try:
        result = proj_service.delete_proj_rich_text(request.form.get('id'))
        return jsonify(status='ok', content=result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/pic", methods=['POST'])
def create_proj_pic():
    try:
        form = request.form
        result = proj_service.create_proj_pic(**form)
        return jsonify(status='ok', content=result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/pic", methods=['DELETE'])
def delete_proj_pic():
    try:
        result = proj_service.delete_proj_pic(request.form.get('id'))
        return jsonify(status='ok', content=result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route('/img/upload', methods=['post'])
def up_photo():
    file = request.files['file']
    file_name = time_util.format_time() + secure_filename(file.filename)
    file_path = app.config['UPLOADED_IMAGES_DEST'] + file_name
    file.save(file_path)
    form = request.form
    file_url = form['prefix'] +file_name
    proj_service.create_proj_pic(form['proj_id'], form['img_type'], file_url, form['override'] == 'true')
    return jsonify(status='ok', url=file_url)
