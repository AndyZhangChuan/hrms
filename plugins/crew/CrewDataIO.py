# -*- coding: utf8 -*-
import collections
import json

from sqlalchemy import or_

from commons.utils import time_util, to_dict
from dao.manager import CrewMgr
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
        input_format = props['input_format']
        records = []
        for line in data['lines']:
            record = {'proj_id': data['proj_id'],'meta': {}}
            for item in input_format.split(','):
                if '|' in item:
                    pair = item.split('|')
                    record[pair[1]] = line[pair[0]] if pair[0] in line else None
                else:
                    record['meta'][item] = line[item]
            record['id_card_num'] = record['id_card_num'].lower()
            record['meta'] = json.dumps(record['meta'])
            crew = CrewMgr.create_override_if_exist(record)
            record['crew_id'] = crew.id
            records.append(record)
        data['records'] = records
        return Output(Output.OK, content=data)

    @staticmethod
    def crew_data_output(props, form, data):
        output_format = props['output_format']
        data['display_format'] = props['display_format']
        page = data['page']
        filters = data['filters']
        filter_condition = {'is_del': 0}
        expressions = []
        search_key = filters['searchKey']
        if search_key:
            expressions = [or_(CrewMgr.model.crew_name == search_key, CrewMgr.model.phone == search_key, CrewMgr.model.id_card_num == search_key, CrewMgr.model.crew_account == search_key)]

        data['count'] = CrewMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page != 0:
            records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10, offset=(page-1)*10, order_list=[CrewMgr.model.create_time.desc()])
        else:
            if data['count'] > 5000: # 数据量过大保护
                records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000, order_list=[CrewMgr.model.create_time.desc()])
            else:
                records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition)
        data['result'] = []
        for record in records:
            record = to_dict(record)
            record['create_time'] = time_util.timestamp2dateString(record['create_time'])
            record['source'] = CrewMgr.translate_source(record['source'])
            record['work_status'] = CrewMgr.translate_work_status(record['work_status'])
            line = collections.OrderedDict()
            for item in output_format.split(','):
                line['id'] = record['id']
                if '|' in item:
                    pair = item.split('|')
                    line[pair[0]] = record[pair[1]] if pair[1] in record else None
            if record['meta']:
                meta = json.loads(record['meta'])
                for key in meta:
                    line[key] = meta[key]
            data['result'].append(line)
        return Output(Output.OK, content=data)

    @staticmethod
    def crew_data_update(props, form, data):
        crew_id = data['crew_id']
        record = CrewMgr.query_first(
            filter_conditions={'id': crew_id, 'is_del': 0}
        )
        if record:
            CrewMgr.delete(record)
        return Output(Output.OK, content=data)