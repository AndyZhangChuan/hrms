# coding=utf-8
import json

from commons.utils import to_dict, time_util
from data.manager import FineMgr, CrewMgr


class FineDao:

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
    def add_occur_time_str(data):
        """
        赔付发生日期yyyy-mm-dd
        """
        if 'occur_time' in data:
            data['occur_time_str'] = time_util.timestamp2dateString(data['occur_time'])

    @staticmethod
    def add_crew_base_info(data):
        """
        获取crew_name和crew_account
        """
        base_info = CrewMgr.get_crew_base_info_by_id(data['crew_id'])
        for key, value in base_info.items():
            data[key] = value

    @staticmethod
    def list_fine_by_occur_time_desc(proj_id, crew_id, start_time, end_time, page, page_size=10):
        """获取项目列表并分页, 根据发生时间倒序排列"""
        filter_condition = {'is_del': 0, 'proj_id': proj_id}
        expressions = []
        if 0 < start_time < end_time:
            expressions = [FineMgr.model.occur_time > start_time,
                           FineMgr.model.occur_time < end_time]
        if crew_id:
            expressions.append(FineMgr.model.crew_id == crew_id)
        count = FineMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page_size > 5000:
            page_size = 5000
        records = FineMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=page_size,
                                offset=(page - 1) * 10, order_list=[FineMgr.model.occur_time.desc()])
        return {'total_count': count, 'datas': to_dict(records)}

    @staticmethod
    def get_fine_by_id(fine_id):
        """通过项目id获取单个项目"""
        return to_dict(FineMgr.get(fine_id))