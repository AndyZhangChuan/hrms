# coding=utf-8
import json
import traceback

from flask import jsonify, request

from core import app
from service import crew_service


@app.route("/crew", methods=['POST'])
def create_crew_record():
    """
    创建赔付记录
    :return:
    """
    try:
        proj_id = int(request.form.get("proj_id", 0))
        lines = request.form.get("lines", None)
        result = crew_service.create_crew_record(proj_id, json.loads(lines))
        return jsonify(status='ok', data=result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/crew", methods=['DELETE'])
def delete_crew_record():
    """
    查找赔付记录
    :return:
    """
    try:
        crew_id = int(request.args.get('crew_id'))
        data = crew_service.delete_crew_record(crew_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/crew", methods=['PUT'])
def update_crew_record():
    """
    查找赔付记录
    :return:
    """
    try:
        crew_id = int(request.form.get('crew_id'))
        content = json.loads(request.form.get('content'))
        crew_service.update_crew_records(crew_id, content)
        return jsonify(status='ok')
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)