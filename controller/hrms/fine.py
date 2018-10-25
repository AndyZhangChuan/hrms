# coding=utf-8
import json
import traceback

from flask import jsonify, request

from controller.decorater import get_request_proj_id
from core import app
from service import fine_service


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


@app.route("/fine", methods=['DELETE'])
def delete_fine_record():
    """
    查找赔付记录
    :return:
    """
    try:
        fine_id = int(request.args.get('fine_id'))
        data = fine_service.delete_fine_records(fine_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)