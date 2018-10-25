# coding=utf-8
import json

from commons.exception import BatchUploadError
from commons.utils import time_util
from data.manager import FineMgr, CrewMgr


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


def delete_fine_records(fine_id):
    record = FineMgr.get(fine_id)
    if record:
        FineMgr.delete(record)