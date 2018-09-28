# coding=utf-8
import json

from sqlalchemy import or_

from core.framework.plugin import execute_proj_plugin
from dao.manager import CrewMgr
from service.constant import proj_nodes


def get_input_format(proj_id):
    data = {}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_INPUT, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def create_crew_record(proj_id, lines):
    return execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_ADD, {}, {'proj_id': proj_id, 'lines': lines, 'errors': []})


def get_crew_records(proj_id, page, filters):
    filter_condition = {'is_del': 0}
    expressions = []
    search_key = filters['searchKey'] if 'searchKey' in filters else None
    if search_key:
        expressions = [or_(CrewMgr.model.crew_name == search_key, CrewMgr.model.phone == search_key,
                           CrewMgr.model.id_card_num == search_key, CrewMgr.model.crew_account == search_key)]
    if 'crew_id' in filters and filters['crew_id']:
        expressions.append(CrewMgr.model.id == filters['crew_id'])
    count = CrewMgr.count(expressions=expressions, filter_conditions=filter_condition)
    if page != 0:
        records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10,
                                offset=(page - 1) * 10, order_list=[CrewMgr.model.create_time.desc()])
    else:
        if count > 5000:  # 数据量过大保护
            records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000,
                                    order_list=[CrewMgr.model.create_time.desc()])
        else:
            records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition)
    data = {'proj_id': proj_id, 'count': count, 'records': records}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_OUTPUT, {}, data)
    data['records'] = None
    data['result'] = json.dumps(data['result'])
    return execute_result


def get_crew_record_by_id(proj_id, crew_id):
    filter_condition = {'id': crew_id, 'is_del': 0}
    record = CrewMgr.query_first(filter_condition)
    if not record:
        return None
    data = {'proj_id': proj_id, 'records': [record]}
    execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_OUTPUT, {}, data)
    return data['result'][0]


def update_crew_records(proj_id, crew_id, content):
    content['crew_id'] = crew_id
    execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_ADD, {}, {'proj_id': proj_id,  'lines': [content], 'errors': []})
    record = get_crew_record_by_id(proj_id, crew_id)
    return record


def delete_crew_record(proj_id, crew_id):
    record = CrewMgr.query_first(
        filter_conditions={'id': crew_id, 'is_del': 0}
    )
    if record:
        CrewMgr.delete(record)
