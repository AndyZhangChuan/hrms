# -*- encoding: utf8 -*-

from core import app
from flask import jsonify

from hrms.dao.manager.hrms.proj import ProjMgr


@app.route("/test", methods=['GET'])
def test():
    proj = ProjMgr.get(1)
    return jsonify(status='ok', proj_name=proj.proj_name)