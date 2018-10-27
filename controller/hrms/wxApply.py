# coding=utf-8
import json
import traceback

from flask import request, jsonify

from core import app
from service import wxApply_service


@app.route("/wxApply", methods=['GET'])
def get_wxapply_record():
    """
    查找赔付记录
    :return:
    """
    try:
        filters = json.loads(request.args.get('filters', '[]'))
        proj_id = request.args.get('proj_id')
        page = int(request.args.get('page'))
        result = wxApply_service.get_apply_records(proj_id, page, filters)
        return jsonify(**result)
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/wxApply", methods=['PUT'])
def update_apply_record():
    try:
        proj_id = request.form.get('proj_id')
        entry_status = request.form.get('entry_status')
        apply_id = int(request.form.get('apply_id'))
        start_time = int(request.form.get('start_time'))
        data = wxApply_service.update_apply_records(proj_id, apply_id, entry_status, start_time)
        return jsonify(status='ok', content=data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)