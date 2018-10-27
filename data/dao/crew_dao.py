# coding=utf-8
import json

from sqlalchemy import or_

from commons.utils import to_dict, time_util
from data.manager import CrewMgr, CrewLevelMgr


class CrewDao:

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
    def add_create_time_str(data):
        """
        员工创建（第一次报名或被导入系统）日期yyyy-mm-dd
        """
        if 'create_time' in data:
            data['create_time_str'] = time_util.timestamp2dateString(data['create_time'])

    @staticmethod
    def add_source_str(data):
        """
        员工来源渠道： 0-网招报名， 1-供应商， 2-员工推荐
        """
        if 'source' in data:
            data['source_str'] = CrewMgr.translate_source(data['source'])

    @staticmethod
    def add_work_status_str(data):
        """
        员工工作状态： 0-空闲， 1-工作中
        """
        if 'work_status' in data:
            data['work_status_str'] = CrewMgr.translate_work_status(data['work_status'])

    @staticmethod
    def add_crew_level_info(data):
        """
        获取crew_name和crew_account
        """
        level = CrewLevelMgr.query_first({'crew_id': data['id'], 'is_del': 0})
        data['accumulate_work_days'] = level.accumulate_work_days
        data['level_name'] = level.level_name

    @staticmethod
    def list_crew_by_create_time_desc(proj_id, search_key, page, page_size=10):
        """获取员工列表并分页, 根据发生时间倒序排列"""
        filter_condition = {'is_del': 0}
        if proj_id:
            filter_condition['proj_id'] = proj_id
        expressions = []
        if search_key:
            expressions = [or_(CrewMgr.model.crew_name == search_key, CrewMgr.model.phone == search_key,
                               CrewMgr.model.id_card_num == search_key, CrewMgr.model.crew_account == search_key)]
        count = CrewMgr.count(expressions=expressions, filter_conditions=filter_condition)
        if page_size > 5000:  # 数据量过大保护
            page_size = 5000
        records = CrewMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=page_size,
                                offset=page_size*(page-1), order_list=[CrewMgr.model.create_time.desc()])
        return {'total_count': count, 'datas': to_dict(records)}

    @staticmethod
    def get_crew_by_id(crew_id):
        """通过员工id获取单个项目"""
        return to_dict(CrewMgr.get(crew_id))