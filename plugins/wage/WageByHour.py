# -*- coding: utf8 -*-

from plugins.plugin import Plugin, Props, Output
from service.constant import proj_nodes as constants


class WageByHour(Plugin):

    __plugin_id__ = 'WageByWHour'
    __plugin_name__ = '纯按时计费'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = {
        constants.WAGE_ON_CALCULATE: '结算时纯按照每小时单价计算',
    }

    unit_price = Props(type='number', default=0, nullable=True, comment='每件单价')

    @staticmethod
    def wage_on_calculate(props, form, data):
        print 'plugin!', 'wage on calculate wage by hour'
        return Output(Output.OK, content=data)