# -*- coding: utf8 -*-
import collections
import json

from commons.utils import time_util, to_dict
from dao.manager import WageMgr
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
        for line in data['lines']:
            record = {'proj_id': data['proj_id'],'meta': {}}
            for item in input_format.split(','):
                if '|' in item:
                    pair = item.split('|')
                    record[pair[1]] = line[pair[0]] if pair[0] in line else None
                else:
                    record['meta'][item] = line[item]
            if 'wage_time' in record:
                record['wage_time'] = time_util.dateString2timestampCommon(record['wage_time'])
            records.append(record)
        data['records'] = records
        return Output(Output.OK, content=data)

    @staticmethod
    def wage_data_output(props, form, data):
        output_format = props['output_format']
        data['display_format'] = props['display_format']
        page = data['page']
        filters = data['filters']
        filter_condition = {'is_del': 0}
        expressions = []
        if 0 < filters['startTime'] < filters['endTime']:
            expressions = [WageMgr.model.wage_time > filters['startTime'], WageMgr.model.wage_time < filters['endTime']]

        data['count'] = WageMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page != 0:
            records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10, offset=(page-1)*10, order_list=[WageMgr.model.wage_time.desc()])
        else:
            if data['count'] > 5000:  # 数据量过大保护
                records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000, order_list=[WageMgr.model.wage_time.desc()])
            else:
                records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition)
        data['result'] = []
        for record in records:
            record = to_dict(record)
            record['wage_time'] = time_util.timestamp2dateString(record['wage_time'])
            line = collections.OrderedDict()
            for item in output_format.split(','):
                if '|' in item:
                    pair = item.split('|')
                    line[pair[0]] = record[pair[1]] if pair[1] in record else None
            if record['meta']:
                meta = json.loads(record['meta'], object_pairs_hook=collections.OrderedDict)
                for key in meta:
                    line[key] = meta[key]
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