# -*- coding: utf8 -*-
import collections
import json

from commons.exception import BatchUploadError
from commons.helper import string_configure_helper
from commons.utils import time_util, to_dict
from data.manager import FineMgr, CrewMgr
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

    @staticmethod
    def fine_data_update(props, form, data):
        fine_id = data['fine_id']
        record = FineMgr.query_first(
            filter_conditions={'id': fine_id, 'is_del': 0}
        )
        if record:
            FineMgr.delete(record)
        return Output(Output.OK, content=data)