# coding=utf-8
from core.framework.plugin import execute_proj_plugin
from dao.manager import FineMgr
from service.constant import proj_nodes


def get_input_format(proj_id):
    data = {}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_INPUT, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def create_fine_record(proj_id, lines):
    data = {'proj_id': proj_id, 'lines': lines, 'errors': []}
    return execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_ADD, {}, data)


def get_fine_records(proj_id, page, filters):
    filter_condition = {'is_del': 0}
    expressions = []
    if 0 < filters['startTime'] < filters['endTime']:
        expressions = [FineMgr.model.occur_time > filters['startTime'], FineMgr.model.occur_time < filters['endTime']]
    if 'crew_id' in filters and filters['crew_id']:
        expressions.append(FineMgr.model.crew_id == filters['crew_id'])
    count = FineMgr.count(expressions=expressions, filter_conditions=filter_condition)
    if page != 0:
        records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10,
                                offset=(page - 1) * 10, order_list=[FineMgr.model.occur_time.desc()])
    else:
        if count > 5000:  # 数据量过大保护
            records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000,
                                    order_list=[FineMgr.model.occur_time.desc()])
        else:
            records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition)
    data = {'proj_id': proj_id, 'count': count, 'records': records}
    result = execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_OUTPUT, {}, data)
    data['records'] = None
    return result


def delete_fine_records(proj_id, fine_id):
    data = {'fine_id': fine_id, 'proj_id': proj_id}
    return execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_UPDATE, {}, data)