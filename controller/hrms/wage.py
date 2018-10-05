# coding=utf-8
import json
import traceback

from flask import jsonify, request

from core import app
from service import wage_service


@app.route("/wage/inputFormat", methods=['GET'])
def wage_data_input_format():
    try:
        proj_id = int(request.args.get("proj_id", 0))
        data = wage_service.get_input_format(proj_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/wage/raw", methods=['POST'])
def create_wage_record():
    """
    创建收入记录
    :return:
    """
    try:
        proj_id = int(request.form.get("proj_id", 0))
        lines = request.form.get("lines", None)
        result = wage_service.create_wage_raw_data(proj_id, json.loads(lines))
        return jsonify(**result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/wage", methods=['GET'])
def get_wage_record():
    """
    查找赔付记录
    :return:
    """
    try:
        filters = json.loads(request.args.get('filters', '[]'))
        proj_id = request.args.get('proj_id')
        page = int(request.args.get('page'))
        result = wage_service.get_wage_records(proj_id, page, filters)
        return jsonify(**result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)

