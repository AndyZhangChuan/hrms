# -*- encoding: utf8 -*-

import sys
from core import app
from controller.decorater.rights import rights
from commons.constants import RightsResourceConstant
reload(sys)
sys.setdefaultencoding('utf8')


@rights(RightsResourceConstant.RIGHTS_MANAGER_ADD)
@app.route("/manager", methods=['POST'])
def add_manager():
    pass


@rights(RightsResourceConstant.RIGHTS_MANAGER_UPDATE)
@app.route("/manager", methods=['PUT'])
def update_manager():
    pass


@rights(RightsResourceConstant.RIGHTS_MANAGER_DETAIL)
@app.route("/manager/<int:manager_id>", methods=['GET'])
def get_manager_detail(manager_id):
    pass


@rights(RightsResourceConstant.RIGHTS_MANAGER_LIST)
@app.route("/manager", methods=['GET'])
def get_manager_detail():
    pass


@app.route("/manager/login", methods=['POST'])
def manager_login():
    pass


@app.route("/manager/forget/psw", methods=['GET'])
def forget_manager_password():
    pass


@app.route("/manager/password", methods=['PUT'])
def update_manager_password():
    pass


@app.route("/manager/role/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_ROLE_ALLOCATE)
def allocate_manager_role():
    pass


@app.route("/manager/proj/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_PROJ_ALLOCATE)
def allocate_manager_proj():
    pass







