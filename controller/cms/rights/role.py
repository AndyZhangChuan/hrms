# -*- encoding: utf8 -*-

import sys
from core import app
from controller.decorater.rights import rights
from commons.constants import RightsResourceConstant
reload(sys)
sys.setdefaultencoding('utf8')


@app.route("/rights/role", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_ROLE_ADD)
def add_rights_role():
    pass


@app.route("/rights/role", methods=['PUT'])
@rights(RightsResourceConstant.RIGHTS_ROLE_UPDATE)
def update_rights_role():
    pass


@app.route("/rights/role/<int:role_id>", methods=['DELETE'])
@rights(RightsResourceConstant.RIGHTS_ROLE_DELETE)
def delete_rights_role(role_id):
    pass


@app.route("/rights/role/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_ROLE_LIST)
def get_rights_role_list():
    pass


@app.route("/rights/role/<int:role_id>", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_ROLE_DETAIL)
def get_rights_role_list(role_id):
    pass


@app.route("/rights/role/allocate", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_ROLE_UPDATE)
def allocate_rights_role():
    pass
