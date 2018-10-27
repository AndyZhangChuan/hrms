# coding=utf-8
from flask import request, jsonify

from core import app
from service import crew_service


@app.route("/crew/apply", methods=['POST'])
def crew_apply():
    """
    项目报名
    :return:
    """
    try:
        proj_id = request.form.get('proj_id')
        crew_id = int(request.form.get('crew_id'))
        data = crew_service.apply_proj(proj_id, crew_id)
        return jsonify(**data)
    except Exception, ex:
        return jsonify(status='error', msg=ex.message)