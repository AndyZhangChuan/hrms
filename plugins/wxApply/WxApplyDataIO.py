# -*- coding: utf8 -*-
import collections
from commons.helper import string_configure_helper
from commons.utils import time_util, to_dict, GetInformation
from data.manager import CrewProjMapMgr, CrewMgr
from plugins.plugin import Plugin, Output, Props
from service.constant import proj_nodes as constants


class WxApplyDataIO(Plugin):

    __plugin_id__   = 'WxApplyDataIO'
    __plugin_name__ = '网招数据IO'
    __category__    = 'crew'
    __priority__    = 100000

    __desc__ = {
        constants.WX_APPLY_DATA_OUTPUT: '定义赔付数据导出格式，以及导出出发的行为，以及列表展示时的字段',
    }

    output_format = Props(type='string', default='', nullable=True, comment='导出字段')
    display_format = Props(type='string', default='', nullable=True, comment='列表展示字段')

    @staticmethod
    def wx_apply_data_output(props, form, data):
        data['display_format'] = props['display_format']
        data['result'] = []
        for record in data['records']:
            crew = CrewMgr.get(record.crew_id)
            if not crew:
                continue
            crew = to_dict(crew)
            crew['create_time'] = time_util.timestamp2dateString(crew['create_time'])
            crew['start_time'] = time_util.timestamp2dateString(record.start_time) if record.start_time else '待定'
            crew['entry_status'] = CrewProjMapMgr.translate_entry_status(record.entry_status)
            crew['age'] = GetInformation(crew['id_card_num']).get_age()
            crew['gender'] = GetInformation(crew['id_card_num']).get_gender_text()
            crew['apply_id'] = record.id
            line = collections.OrderedDict()
            string_configure_helper.explain(props['output_format'], crew, line)
            data['result'].append(line)
        return Output(Output.OK, content=data)