# -*- encoding: utf8 -*-
import traceback

from werkzeug.utils import secure_filename

from core import app
from flask import jsonify
from flask import request
from service import proj_service
from commons.utils import web_util, time_util


@app.route("/proj", methods=['POST'])
def create_proj():
    """
    创建项目
    :return:
    """
    try:
        data = proj_service.create_proj(request.form)
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/<int:proj_id>", methods=['PUT'])
def update_proj(proj_id):
    """
    更改项目
    :return:
    """
    try:
        data = proj_service.update_proj(proj_id, request.form)
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/proj/<int:proj_id>", methods=['DELETE'])
def delete_proj(proj_id):
    try:
        data = proj_service.delete_proj(proj_id)
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
        return jsonify(status='ok', data=result)
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


@app.route("/offer", methods=['POST'])
def create_offer():
    """
    创建项目
    :return:
    """
    try:
        data = proj_service.create_offer(request.form)
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/offer/<int:offer_id>", methods=['PUT'])
def update_offer(offer_id):
    """
    更改项目
    :return:
    """
    try:
        data = proj_service.update_offer(offer_id, request.form)
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/post/<int:post_id>", methods=['PUT'])
def update_post(post_id):
    """
    更改项目
    :return:
    """
    try:
        data = proj_service.update_post(post_id, request.form)
        return jsonify(data)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)
