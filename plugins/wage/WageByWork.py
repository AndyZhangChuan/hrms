# -*- coding: utf8 -*-

from plugins import Plugin, Props, Output
from service.constant import proj_nodes as constants


class WageByWork(Plugin):

    __plugin_id__ = 'WageByWork'
    __plugin_name__ = '纯按件计费'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = {
        constants.WAGE_ON_CALCULATE: '结算时纯按照每件单价计算',
    }

    unit_price = Props(type='number', default=1, nullable=True, comment='每件单价')

    @staticmethod
    def wage_on_calculate(props, form, data):
        print 'plugin!', 'wage on calculate wage by work'
        return Output(Output.OK, content=data)