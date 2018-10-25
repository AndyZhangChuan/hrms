# -*- coding: utf8 -*-

from plugins.plugin import Plugin, Props, Output


class WageByWork3levels(Plugin):

    __plugin_id__ = 'WageByWork3levels'
    __plugin_name__ = '三级按件计费'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = '标准件数以下部分按标准单价计算，标准件数至一级件数部分按一级单价计算，一级件数至二级件数部分按二级单价计算，以此类推，三级件数以上按三级单价计算'

    standard_amount = Props(type='int', default=0, nullable=True, comment='标准件数')
    standard_price = Props(type='float', default=0.00, nullable=True, comment='标准单价')
    lv1_amount = Props(type='int', default=0, nullable=True, comment='一级件数')
    lv1_price = Props(type='float', default=0.00, nullable=True, comment='一级单价')
    lv2_amount = Props(type='int', default=0, nullable=True, comment='二级件数')
    lv2_price = Props(type='float', default=0.00, nullable=True, comment='二级单价')
    lv3_amount = Props(type='int', default=0, nullable=True, comment='三级件数')
    lv3_price = Props(type='float', default=0.00, nullable=True, comment='三级单价')

    @staticmethod
    def wage_on_calculate(props, form, data):

        return Output(Output.OK, content=data)

