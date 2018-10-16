# coding=utf-8
import json

from sqlalchemy import or_

from commons.utils import to_dict
from core.framework.plugin import execute_proj_plugin
from data.manager import CrewProjMapMgr, CrewMgr
from service.constant import proj_nodes


def get_apply_records(proj_id, page, filters):
    filter_condition = {'proj_id': proj_id, 'is_del': 0}
    expressions = []
    search_key = filters['searchKey'] if 'searchKey' in filters else None
    if search_key:
        crew_expression = [or_(CrewMgr.model.crew_name == search_key, CrewMgr.model.phone == search_key,
                           CrewMgr.model.id_card_num == search_key, CrewMgr.model.crew_account == search_key)]
        search_crews = CrewMgr.query({'is_del': 0}, expressions=crew_expression)
        search_crew_ids = [item.id for item in search_crews]
        expressions.append(CrewProjMapMgr.model.crew_id.in_(search_crew_ids))
    if 'crew_id' in filters and filters['crew_id']:
        expressions.append(CrewProjMapMgr.model.crew_id == filters['crew_id'])
    if 'entry_status' in filters:
        expressions.append(CrewProjMapMgr.model.entry_status == filters['entry_status'])
    count = CrewProjMapMgr.count(expressions=expressions, filter_conditions=filter_condition)
    if page != 0:
        records = CrewProjMapMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10,
                                offset=(page - 1) * 10, order_list=[CrewProjMapMgr.model.create_time.desc()])
    else:
        if count > 5000:  # 数据量过大保护
            records = CrewProjMapMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000,
                                    order_list=[CrewProjMapMgr.model.create_time.desc()])
        else:
            records = CrewProjMapMgr.query(expressions=expressions, filter_conditions=filter_condition)
    data = {'proj_id': proj_id, 'count': count, 'records': records}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WX_APPLY_DATA_OUTPUT, {}, data)
    data['records'] = None
    data['result'] = json.dumps(data['result'])
    return execute_result


def apply_proj(proj_id, crew_id):
    proj = CrewProjMapMgr.query_first({'crew_id': crew_id, 'proj_id': proj_id, 'is_del': 0})
    if proj:
        if proj.entry_status == 0:
            return dict(status='error', message='已经申请该职位，请等待审核结果')
        elif proj.entry_status == 1:
            return dict(status='error', message='已经成功申请到该职位，请联系您的负责人准备工作吧')
        elif proj.entry_status == 2:
            return dict(status='error', message='申请被拒绝，暂时无法再次申请')
    else:
        return dict(status='ok', content=to_dict(CrewProjMapMgr.create(crew_id=crew_id, proj_id=proj_id)))


def update_apply_records(proj_id, apply_id, entry_status, start_time):
    record = CrewProjMapMgr.query_first(
        filter_conditions={'id': apply_id, 'is_del': 0}
    )
    if record:
        CrewProjMapMgr.update(record, entry_status=entry_status, start_time=start_time)