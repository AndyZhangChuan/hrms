# -*- coding: utf8 -*-
import collections
import json

from commons.helper import string_configure_helper
from commons.utils import time_util, to_dict
from data.manager import CrewMgr
from plugins.plugin import Plugin, Output, Props
from service.constant import proj_nodes as constants


class CrewDataIO(Plugin):

    __plugin_id__   = 'CrewDataIO'
    __plugin_name__ = '员工数据IO'
    __category__    = 'crew'
    __priority__    = 100000

    __desc__ = {
        constants.CREW_DATA_INPUT: '定义赔付数据导入格式，以及导入后触发的行为。此插件在导入后进记录，不触发其他行为',
        constants.CREW_DATA_ADD: '新增赔付记录',
        constants.CREW_DATA_OUTPUT: '定义赔付数据导出格式，以及导出出发的行为，以及列表展示时的字段',
        constants.CREW_DATA_UPDATE: '赔付数据更改（只有撤销）',
    }

    input_format = Props(type='string', default='', nullable=True, comment='导入字段')
    input_template = Props(type='string', default='', nullable=True, comment='导入模版')
    output_format = Props(type='string', default='', nullable=True, comment='导出字段')
    display_format = Props(type='string', default='', nullable=True, comment='列表展示字段')

    @staticmethod
    def crew_data_input(props, form, data):
        data['input_format'] = props['input_format']
        data['input_template'] = props['input_template']
        return Output(Output.OK, content=data)

    @staticmethod
    def crew_data_add(props, form, data):
        records = []
        line_index = 0
        for line in data['lines']:
            line_index += 1
            record = {'proj_id': data['proj_id'],'meta': {}}
            string_configure_helper.load(props['input_format'], line, record)
            record['id_card_num'] = record['id_card_num'].lower()
            record['meta'] = json.dumps(record['meta'])
            record['crew_id'] = line['crew_id'] if 'crew_id' in line else ''
            crew = CrewMgr.create_override_if_exist(record)
            record['crew_id'] = crew.id
            # data['errors'].append(BatchUploadError(line_index, line, '该员工没有录入系统').to_dict())
            records.append(record)
        data['records'] = records
        return Output(Output.OK, content=data)

    @staticmethod
    def crew_data_output(props, form, data):
        data['display_format'] = props['display_format']
        data['result'] = []
        for record in data['records']:
            record = to_dict(record)
            record['create_time'] = time_util.timestamp2dateString(record['create_time'])
            record['source'] = CrewMgr.translate_source(record['source'])
            record['work_status'] = CrewMgr.translate_work_status(record['work_status'])
            line = collections.OrderedDict()
            string_configure_helper.explain(props['output_format'], record, line)
            data['result'].append(line)
        return Output(Output.OK, content=data)