# -*- coding: utf8 -*-

from hrms.plugins.plugin import Plugin, Props, Output
from hrms.commons.constant import proj_nodes as constants

class CrewBasic(Plugin):

    __plugin_id__ = 'CrewBasic'
    __plugin_name__ = '基础员工'
    __category__    = 'crew'
    __priority__    = 100000

    __desc__ = {
        constants.CREW_ON_ATTRIBUTES: '员工基础信息（姓名，身份证，手机号',
    }

    # unit_price = Props(type='number', default=0, nullable=True, comment='每件单价')

    @staticmethod
    def crew_on_attributes(props, form, data):
        print 'plugin!', 'crew on attributes crew basic'
        return Output(Output.OK, content=data)