# -*- coding: utf8 -*-
import collections
import json
import time

from dao.manager import CrewLevelMgr
from plugins.plugin import Plugin, Props, Output
from service.constant import proj_nodes as constants


class CrewLevelStrategyA(Plugin):

    __plugin_id__ = 'CrewLevelStrategyA'
    __plugin_name__ = '人员等级制A'
    __category__    = 'crew'
    __priority__    = 100000

    __desc__ = {
        constants.CREW_DATA_ADD: '对人员信息处理，并初始化人员等级',
    }

    @staticmethod
    def crew_data_add(props, form, data):
        records = data['records']
        for record in records:
            level = CrewLevelMgr.query_first({'crew_id': record['crew_id'], 'is_del': 0})
            if not level:
                CrewLevelMgr.create(crew_id=record['crew_id'], crew_name=record['crew_name'], level_name='青铜')
        return Output(Output.OK, content=data)

    @staticmethod
    def crew_data_output(props, form, data):
        for record in data['result']:
            level = CrewLevelMgr.query_first({'crew_id': record['id'], 'is_del': 0})
            record['累计天数'] = level.accumulate_work_days
            record['等级'] = level.level_name
        return Output(Output.OK, content=data)
