# -*- encoding: utf8 -*-

import sys
from core import app
from controller.decorater.rights import rights
from commons.constants import RightsResourceConstant
reload(sys)
sys.setdefaultencoding('utf8')


@app.route("/rights", methods=['POST'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_ADD)
def add_rights_resource():
    pass


@app.route("/rights", methods=['PUT'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_UPDATE)
def update_rights_resource():
    pass


@app.route("/rights/<int:resource_id>", methods=['DELETE'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_DELETE)
def delete_rights_resource(resource_id):
    pass


@app.route("/rights/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_LIST)
def get_rights_resource_list():
    pass


@app.route("/rights/<int:resource_id>", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_DETAIL)
def get_rights_resource_detail(resource_id):
    pass


@app.route("/rights/editable/list", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_RESOURCE_LIST)
def get_rights_resource_detail():
    pass


@app.route("/rights/uiElements/byParentId", methods=['GET'])
@rights(RightsResourceConstant.RIGHTS_MANAGER_LOGIN)
def get_rights_resource_detail():
    pass


