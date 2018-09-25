import json

from core.framework.plugin import execute_proj_plugin
from service.constant import proj_nodes


def get_input_format(proj_id):
    data = {}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_INPUT, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def create_crew_record(proj_id, lines):
    execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_ADD, {}, {'proj_id': proj_id, 'lines': lines})


def get_crew_records(proj_id, page, filters):
    data = {'proj_id': proj_id, 'page': page, 'filters': filters}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_OUTPUT, {}, data)
    data['result'] = json.dumps(data['result'])
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def delete_crew_records(proj_id, crew_id):
    data = {'crew_id': crew_id, 'proj_id': proj_id}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.CREW_DATA_UPDATE, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data