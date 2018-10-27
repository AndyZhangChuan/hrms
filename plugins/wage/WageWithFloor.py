# -*- coding: utf8 -*-

from plugins.plugin import Plugin, Props, Output
from service.constant import proj_nodes as constants


class WageWithFloor(Plugin):

    __plugin_id__ = 'WageWithFloor'
    __plugin_name__ = '保底工资'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = '当员工在保底期内，实际收入不会低于保底工资'

    floor_wage = Props(type='int', default=0, nullable=True, comment='保底工资')
    protect_days = Props(type='int', default=0, nullable=True, comment='保底期天数')

    @staticmethod
    def wage_on_calculate(props, form, data):
        print 'plugin!', 'wage on calculate wage by hour'
        return Output(Output.OK, content=data)