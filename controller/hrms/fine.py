# coding=utf-8
import json
import traceback

from flask import jsonify, request

from controller.decorater import get_request_proj_id
from core import app
from service import fine_service


@app.route("/fine/inputFormat", methods=['GET'])
def fine_data_input_format():
    try:
        proj_id = get_request_proj_id()
        data = fine_service.get_input_format(proj_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/fine", methods=['POST'])
def create_fine_record():
    """
    创建赔付记录
    :return:
    """
    try:
        proj_id = get_request_proj_id()
        lines = request.form.get("lines", None)
        result = fine_service.create_fine_record(proj_id, json.loads(lines))
        return jsonify(status='ok', data=result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/fine", methods=['GET'])
def get_fine_record():
    """
    查找赔付记录
    :return:
    """
    try:
        filters = json.loads(request.args.get('filters', '[]'))
        proj_id = get_request_proj_id()
        result = fine_service.get_fine_records(proj_id, filters)
        return jsonify(**result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/fine", methods=['DELETE'])
def delete_fine_record():
    """
    查找赔付记录
    :return:
    """
    try:
        proj_id = get_request_proj_id()
        fine_id = int(request.args.get('fine_id'))
        data = fine_service.delete_fine_records(proj_id, fine_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)