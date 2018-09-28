# coding=utf-8
import json
import traceback

from flask import jsonify, request

from core import app
from service import crew_service


@app.route("/crew/inputFormat", methods=['GET'])
def crew_data_input_format():
    try:
        proj_id = int(request.args.get("proj_id", 0))
        data = crew_service.get_input_format(proj_id)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


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
        return jsonify(**result)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)


@app.route("/crew", methods=['GET'])
def get_crew_record():
    """
    查找赔付记录
    :return:
    """
    try:
        filters = json.loads(request.args.get('filters', '[]'))
        proj_id = request.args.get('proj_id')
        page = int(request.args.get('page'))
        result = crew_service.get_crew_records(proj_id, page, filters)
        return jsonify(**result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/crew", methods=['DELETE'])
def delete_crew_record():
    """
    查找赔付记录
    :return:
    """
    try:
        proj_id = request.args.get('proj_id')
        crew_id = int(request.args.get('crew_id'))
        data = crew_service.delete_crew_record(proj_id, crew_id)
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
        proj_id = request.form.get('proj_id')
        crew_id = int(request.form.get('crew_id'))
        content = json.loads(request.form.get('content'))
        data = crew_service.update_crew_records(proj_id, crew_id, content)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)