# -*- coding: utf8 -*-
import collections
import json
import time

from plugins.plugin import Plugin, Props, Output
from service.constant import proj_nodes as constants


class WageByWorkJD(Plugin):

    __plugin_id__ = 'WageByWorkJD'
    __plugin_name__ = '纯按件计费(京东）'
    __category__    = 'wage'
    __priority__    = 100000

    __desc__ = {
        constants.WAGE_DATA_ADD: '对导入的数据做结算处理，并对导入字段进行加工，处理后字段放在meta里',
    }

    jh_price = Props(type='float', default=1, nullable=True, comment='拣货单价')
    jh_standard = Props(type='int', default=1, nullable=True, comment='拣货标准')
    fh_price = Props(type='float', default=1, nullable=True, comment='复核单价')
    fh_standard = Props(type='int', default=1, nullable=True, comment='复核标准')
    yth_price = Props(type='float', default=1, nullable=True, comment='一体化打包单价')
    yth_standard = Props(type='int', default=1, nullable=True, comment='一体化打包标准')
    fyth_price = Props(type='float', default=1, nullable=True, comment='非一体化打包单价')
    fyth_standard = Props(type='int', default=1, nullable=True, comment='非一体化打包标准')

    @staticmethod
    def wage_data_add(props, form, data):
        records = data['records']
        data['wage_raw_datas'] = []
        data['wage'] = []
        for record in records:
            line = record['meta']
            total_amount = 0
            wage_meta = collections.OrderedDict()
            wage_meta['工作时长'] = record['work_hours']
            bus_id = '%s%s%s' % (record['proj_id'], record['crew_account'], record['wage_time'])

            jh_amount = float(line[u'拣货件数']) if u'拣货件数' in line and line[u'拣货件数'] else 0
            fh_amount = float(line[u'复核件数']) if u'复核件数' in line and line[u'复核件数'] else 0
            yth_amount = float(line[u'打包一体化单量']) if u'打包一体化单量' in line and line[u'打包一体化单量'] else 0
            fyth_amount = float(line[u'打包非一体化单量']) if u'打包非一体化单量' in line and line[u'打包非一体化单量'] else 0
            jh_standard = props['jh_standard']
            fh_standard = props['fh_standard']
            yth_standard = props['yth_standard']
            fyth_standard = props['fyth_standard']

            wage_meta['拣货件数'] = jh_amount
            wage_meta['拣货标准件数'] = jh_standard
            wage_meta['拣货达标效率'] = round(jh_amount / jh_standard, 2)
            wage_meta['复核件数'] = fh_amount
            wage_meta['复核标准件数'] = fh_standard
            wage_meta['复核达标效率'] = round(fh_amount / fh_standard, 2)
            wage_meta['打包一体化单量'] = yth_amount
            wage_meta['打包一体化标准单量'] = yth_standard
            wage_meta['打包一体化达标效率'] = round(yth_amount / yth_standard, 2)
            wage_meta['打包非一体化单量'] = fyth_amount
            wage_meta['打包非一体化标准单量'] = fyth_standard
            wage_meta['打包非一体化达标效率'] = round(fyth_amount / fyth_standard, 2)

            if jh_amount > 0:
                raw_item = set_raw_item(record, '拣货', bus_id, jh_amount)
                data['wage_raw_datas'].append(raw_item)
                total_amount += jh_amount * props['jh_price']
            if fh_amount > 0:
                raw_item = set_raw_item(record, '复核', bus_id, fh_amount)
                data['wage_raw_datas'].append(raw_item)
                total_amount += fh_amount * props['fh_price']
            if yth_amount > 0:
                raw_item = set_raw_item(record, '打包一体化', bus_id, yth_amount)
                data['wage_raw_datas'].append(raw_item)
                total_amount += yth_amount * props['yth_price']
            if fyth_amount > 0:
                raw_item = set_raw_item(record, '打包非一体化', bus_id, fyth_amount)
                data['wage_raw_datas'].append(raw_item)
                total_amount += fyth_amount * props['fyth_price']

            wage = record.copy()
            wage['bus_id'] = bus_id
            wage['amount'] = total_amount
            wage['meta'] = wage_meta
            wage['confirm_time'] = time.time()
            wage['wage_time'] = record['wage_time']
            data['wage'].append(wage)
        return Output(Output.OK, content=data)


def set_raw_item(line, position, bus_id, amount):
    raw_item = line.copy()
    raw_item['position'] = position
    raw_item['bus_id'] = bus_id
    raw_item['work_amount'] = amount
    return raw_item

