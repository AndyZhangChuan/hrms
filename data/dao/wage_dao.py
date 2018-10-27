# coding=utf-8
import json

from commons.utils import to_dict, time_util
from data.manager import WageMgr, CrewMgr


class WageDao:

    @staticmethod
    def add_meta_data(data):
        """
        获取并解析meta字段中的参数
        """
        if 'meta' in data:
            meta = json.loads(data['meta'])
            for key, value in meta.items():
                data[key] = value

    @staticmethod
    def add_wage_time_str(data):
        """
        工作数据产生日期yyyy-mm-dd
        """
        if 'create_time' in data:
            data['wage_time_str'] = time_util.timestamp2dateString(data['wage_time'])

    @staticmethod
    def add_crew_base_info(data):
        """
        获取crew_name和crew_account
        """
        base_info = CrewMgr.get_crew_base_info_by_id(data['crew_id'])
        for key, value in base_info.items():
            data[key] = value

    @staticmethod
    def list_wage_by_wage_time_desc(proj_id, crew_id, start_time, end_time, page, page_size=10):
        """获取结算列表并分页, 根据实际工作时间倒序排列"""
        filter_condition = {'is_del': 0, 'proj_id': proj_id}
        expressions = []
        if 0 < start_time < end_time:
            expressions = [WageMgr.model.wage_time > start_time,
                           WageMgr.model.wage_time < end_time]
        if crew_id:
            expressions.append(WageMgr.model.crew_id == crew_id)
        count = WageMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page_size > 5000:
            page_size = 5000
        records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=page_size,
                                offset=(page - 1) * 10, order_list=[WageMgr.model.wage_time.desc()])
        return {'total_count': count, 'datas': to_dict(records)}

    @staticmethod
    def get_wage_by_id(wage_id):
        """通过结算记录id获取单条记录"""
        return to_dict(WageMgr.get(wage_id))