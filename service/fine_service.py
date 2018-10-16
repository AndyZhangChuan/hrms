# coding=utf-8
import json

from commons.exception import BatchUploadError
from commons.utils import time_util
from core.framework.plugin import execute_proj_plugin
from data.manager import FineMgr, CrewMgr
from service.constant import proj_nodes


def get_input_format(proj_id):
    data = {}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_INPUT, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def create_fine_record(proj_id, lines):
    errors = []
    line_index = 0
    for line in lines:
        line_index += 1
        record = {'proj_id': proj_id, 'meta': {}}
        for key, value in line.items():
            line[key] = value.strip()
            if key in FineMgr.params:
                record[key] = value
            else:
                record['meta'][key] = value
        if 'occur_time' in record:
            record['occur_time'] = time_util.dateString2timestampCommon(line['occur_time'])
        if 'bill_id' not in line:
            errors.append(BatchUploadError(line_index, '缺少异常单号').to_dict())
            continue
        crew_id = CrewMgr.get_crew_id_by_account(line['crew_account'])
        if not crew_id:
            errors.append(BatchUploadError(line_index, '该员工没有录入系统').to_dict())
            continue
        else:
            record['crew_id'] = crew_id
        record['meta'] = json.dumps(record['meta'])
        FineMgr.create_override_if_exist(record)
    return {'errors': errors, 'lines': lines}



def delete_fine_records(proj_id, fine_id):
    data = {'fine_id': fine_id, 'proj_id': proj_id}
    return execute_proj_plugin(proj_id, proj_nodes.FINE_DATA_UPDATE, {}, data)