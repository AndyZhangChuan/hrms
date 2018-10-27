import traceback

from flask import request, jsonify

from commons.utils import to_dict
from controller.decorater import get_request_proj_id
from core import app
from data.manager import FeConfigureMgr, DaoRelationMapMgr

import data.dao as daos
from inspect import getmembers, isfunction


@app.route("/feconfigure", methods=['GET'])
def get_fe_configure():
    try:
        proj_id = get_request_proj_id()
        page_url = request.args.get("page_url")
        if not page_url:
            config_list = FeConfigureMgr.query({'proj_id': proj_id, 'is_del': 0})
        else:
            config_list = FeConfigureMgr.query({'proj_id': proj_id, 'page_url': page_url, 'is_del': 0})
        return jsonify(status='ok', data=to_dict(config_list))
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/feconfigure", methods=['POST'])
def update_fe_configure():
    try:
        proj_id = get_request_proj_id()
        page_url = request.form.get("page_url")
        gear_id = request.form.get('gear_id')
        props = request.form.get('props')
        props_format = request.form.get('props_format')
        config = FeConfigureMgr.create_or_update(proj_id, page_url, gear_id, props, props_format)
        return jsonify(status='ok', data=to_dict(config))
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/feconfigure", methods=['DELETE'])
def delete_fe_configure():
    try:
        id = int(request.form.get("id"))
        config = FeConfigureMgr.get(id)
        FeConfigureMgr.delete(config)
        return jsonify(status='ok')
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/data/getter", methods=['GET'])
def get_data_getter():
    try:
        items = DaoRelationMapMgr.query({'is_del': 0})
        return jsonify(status='ok', data=to_dict(items))
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)


@app.route("/data/getter/refresh", methods=['GET'])
def refresh_data_getter():
    try:

        members = getmembers(daos)
        dao_list = DaoRelationMapMgr.query({'is_del': 0})
        remote_dao_map = {item.dao + item.type + item.attr_name: item for item in dao_list}
        for member in members:
            dao_name = member[0]
            if dao_name == 'dao_map':
                dao_map = member[1]
                for (key, value) in dao_map.items():
                    module_name = key
                    dao_obj = getmembers(value, isfunction)
                    for item in dao_obj:
                        function_code = item[1].func_code
                        function_type = item[0].split('_')[0]
                        dao_relation_map = {
                            'dao': module_name,
                            'comment': item[1].func_doc,
                            'type': function_type
                        }
                        if function_type in ['get', 'list']:
                            dao_relation_map['attr_name'] = item[0]
                            dao_relation_map['input_args'] = ','.join(
                                function_code.co_varnames[0: function_code.co_argcount])

                        else:
                            dao_relation_map['attr_name'] = item[0].split('_', 1)[1]
                            dao_relation_map['input_args'] = ','.join(
                                function_code.co_varnames[0: function_code.co_argcount - 1])
                        if module_name + function_type + dao_relation_map['attr_name'] not in remote_dao_map:
                            DaoRelationMapMgr.create(**dao_relation_map)
                        else:
                            DaoRelationMapMgr.update(
                                remote_dao_map[module_name + function_type + dao_relation_map['attr_name']],
                                **dao_relation_map)
        return jsonify(status='ok')
    except Exception, ex:
        traceback.print_exc()
        return jsonify(status='error', msg=ex.message)
