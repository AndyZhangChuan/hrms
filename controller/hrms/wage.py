# coding=utf-8
import json
import traceback

from flask import jsonify, request

from core import app
from service import wage_service


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
