# -*- coding: utf8 -*-

from plugins import Plugin, Output
from service.constant import proj_nodes as constants


class ProjBasic(Plugin):

    __plugin_id__ = 'ProjBasic'
    __plugin_name__ = '基础项目'
    __category__    = 'proj'
    __priority__    = 100000

    __desc__ = {
        constants.PROJ_ON_ATTRIBUTES: '项目基础信息：人数，收入，消息',
    }

    # unit_price = Props(type='number', default=0, nullable=True, comment='每件单价')

    @staticmethod
    def proj_on_attributes(props, form, data):
        print 'plugin!', 'proj on attributes proj basic'
        data['work_crew_num'] = 100
        data['current_month_income'] = '30000元'
        data['message_count'] = 3
        return Output(Output.OK, content=data)