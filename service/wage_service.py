# coding=utf-8
import json

from commons.exception import BatchUploadError
from commons.utils import time_util
from data.manager import WageMgr, WageRawDataMgr, CrewMgr


def create_wage_raw_data(proj_id, lines):
    line_index = 0
    data = {'errors': []}
    for line in lines:
        line_index += 1
        record = {'proj_id': data['proj_id'], 'meta': {}}
        for key, value in line.items():
            line[key] = value.strip()
            if key in WageMgr.params:
                record[key] = value
            else:
                record['meta'][key] = value
        if 'wage_time' in record:
            record['wage_time'] = time_util.dateString2timestampCommon(record['wage_time'])
        crew_id = CrewMgr.get_crew_id_by_account(line['crew_account'])
        if not crew_id:
            data['errors'].append(BatchUploadError(line_index, '该员工没有录入系统').to_dict())
            continue
        else:
            record['crew_id'] = crew_id

    for record in data['wage_raw_datas']:
        record['meta'] = json.dumps(record['meta'])
        WageRawDataMgr.create_override_if_exist(record)
    for record in data['wage']:
        record['meta'] = json.dumps(record['meta'])
        WageMgr.create_override_if_exist(record)


