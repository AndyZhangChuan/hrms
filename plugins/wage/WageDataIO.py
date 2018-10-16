# -*- coding: utf8 -*-
import collections
import json

from commons.exception import BatchUploadError
from commons.helper import string_configure_helper
from commons.utils import time_util, to_dict
from data.manager import WageMgr, CrewMgr
from plugins.plugin import Plugin, Output, Props
from service.constant import proj_nodes as constants


class WageDataIO(Plugin):

    __plugin_id__   = 'WageDataIO'
    __plugin_name__ = '结算数据IO'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = {
        constants.WAGE_DATA_INPUT: '定义结算数据导入格式',
        constants.WAGE_DATA_ADD: '读取导入的字段，转化为wage表固定字段',
        constants.WAGE_DATA_OUTPUT: '定义赔付数据导出格式，以及导出出发的行为，以及列表展示时的字段',
        constants.WAGE_DATA_UPDATE: '赔付数据更改（只有撤销）',
    }

    input_format = Props(type='string', default='', nullable=True, comment='导入字段')
    input_template = Props(type='string', default='', nullable=True, comment='导入模版')
    output_format = Props(type='string', default='', nullable=True, comment='导出字段')
    display_format = Props(type='string', default='', nullable=True, comment='列表展示字段')

    @staticmethod
    def wage_data_input(props, form, data):
        data['input_format'] = props['input_format']
        data['input_template'] = props['input_template']
        return Output(Output.OK, content=data)

    @staticmethod
    def wage_data_add(props, form, data):
        input_format = props['input_format']
        records = []
        line_index = 0
        for line in data['lines']:
            line_index += 1
            record = {'proj_id': data['proj_id'],'meta': {}}
            string_configure_helper.load(input_format, line, record)
            if 'wage_time' in record:
                record['wage_time'] = time_util.dateString2timestampCommon(record['wage_time'])
            crew_id = CrewMgr.get_crew_id_by_account(record['crew_account'])
            if not crew_id:
                data['errors'].append(BatchUploadError(line_index, '该员工没有录入系统').to_dict())
                continue
            else:
                record['crew_id'] = crew_id
            records.append(record)
        data['records'] = records
        return Output(Output.OK, content=data)

    @staticmethod
    def wage_data_output(props, form, data):
        data['display_format'] = props['display_format']
        data['result'] = []
        for record in data['records']:
            record = to_dict(record)
            base_info = CrewMgr.get_crew_base_info_by_id(record['crew_id'])
            record = dict(record, **base_info)
            record['wage_time'] = time_util.timestamp2dateString(record['wage_time'])
            line = collections.OrderedDict()
            string_configure_helper.explain(props['output_format'], record, line)
            data['result'].append(line)
        return Output(Output.OK, content=data)

    @staticmethod
    def wage_data_update(props, form, data):
        # fine_id = data['fine_id']
        # record = FineMgr.query_first(
        #     filter_conditions={'id': fine_id, 'is_del': 0}
        # )
        # if record:
        #     FineMgr.delete(record)
        return Output(Output.OK, content=data)