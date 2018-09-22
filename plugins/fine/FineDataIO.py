# -*- coding: utf8 -*-
import collections
import json

from commons.utils import time_util, to_dict
from dao.manager import FineMgr
from plugins.plugin import Plugin, Output, Props
from service.constant import proj_nodes as constants


class FineDataIO(Plugin):

    __plugin_id__   = 'FineDataIO'
    __plugin_name__ = '赔付数据IO'
    __category__    = 'fine'
    __priority__    = 100000

    __desc__ = {
        constants.FINE_DATA_INPUT: '定义赔付数据导入格式，以及导入后触发的行为。此插件在导入后进记录，不触发其他行为',
        constants.FINE_DATA_ADD: '新增赔付记录',
        constants.FINE_DATA_OUTPUT: '定义赔付数据导出格式，以及导出出发的行为，以及列表展示时的字段',
        constants.FINE_DATA_UPDATE: '赔付数据更改（只有撤销）',
    }

    input_format = Props(type='string', default='', nullable=True, comment='导入字段')
    input_template = Props(type='string', default='', nullable=True, comment='导入模版')
    output_format = Props(type='string', default='', nullable=True, comment='导出字段')
    display_format = Props(type='string', default='', nullable=True, comment='列表展示字段')

    @staticmethod
    def fine_data_input(props, form, data):
        data['input_format'] = props['input_format']
        data['input_template'] = props['input_template']
        return Output(Output.OK, content=data)

    @staticmethod
    def fine_data_add(props, form, data):
        input_format = props['input_format']
        for line in data['lines']:
            record = {'proj_id': data['proj_id'],'meta': {}}
            for item in input_format.split(','):
                if '|' in item:
                    pair = item.split('|')
                    record[pair[1]] = line[pair[0]] if pair[0] in line else None
                else:
                    record['meta'][item] = line[item]
            if 'occur_time' in record:
                record['occur_time'] = time_util.dateString2timestampCommon(record['occur_time'])
            record['meta'] = json.dumps(record['meta'])
            FineMgr.create_override_if_exist(record)
        return Output(Output.OK, content=data)

    @staticmethod
    def fine_data_output(props, form, data):
        output_format = props['output_format']
        data['display_format'] = props['display_format']
        page = data['page']
        filters = data['filters']
        filter_condition = {'is_del': 0}
        expressions = []
        if 0 < filters['startTime'] < filters['endTime']:
            expressions = [FineMgr.model.occur_time > filters['startTime'], FineMgr.model.occur_time < filters['endTime']]

        data['count'] = FineMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page != 0:
            records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10, offset=(page-1)*10, order_list=[FineMgr.model.occur_time.desc()])
        else:
            if data['count'] > 5000: # 数据量过大保护
                records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000, order_list=[FineMgr.model.occur_time.desc()])
            else:
                records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition)
        data['result'] = []
        for record in records:
            record = to_dict(record)
            record['occur_time'] = time_util.timestamp2dateString(record['occur_time'])
            line = collections.OrderedDict()
            for item in output_format.split(','):
                if '|' in item:
                    pair = item.split('|')
                    line[pair[0]] = record[pair[1]] if pair[1] in record else None
            if record['meta']:
                meta = json.loads(record['meta'])
                for key in meta:
                    line[key] = meta[key]
            data['result'].append(line)
        data['result'] = json.dumps(data['result'])
        return Output(Output.OK, content=data)

    @staticmethod
    def fine_data_update(props, form, data):
        fine_id = data['fine_id']
        record = FineMgr.query_first(
            filter_conditions={'id': fine_id, 'is_del': 0}
        )
        if record:
            FineMgr.delete(record)
        return Output(Output.OK, content=data)