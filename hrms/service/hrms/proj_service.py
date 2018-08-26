# -*- encoding: utf8 -*-

from hrms.dao.manager.hrms.proj import ProjMgr
from hrms.dao.manager.hrms.proj import ProjPicMgr
from hrms.dao.manager.hrms.proj import ProjOpLogMgr
from hrms.dao.manager.hrms import CompanyMgr
from hrms.commons.constant import proj_constant
from hrms.commons.utils import page_util


def create_proj(operator_id, form):

    # 创建项目信息
    proj_params = {
        'proj_name': form.proj_name.data,
        'company_id': form.company_id.data,
        'address': form.address.data,
        'crew_num': form.crew_num.data,
        'description': form.description.data,
        'category': form.category.data
    }
    proj = ProjMgr.create(**proj_params)

    # 创建项目图片信息
    pic_url_list = form.pic_url_list.data.split(';')
    pic_params = []
    for pic_url in pic_url_list:
        pic_params.append({
            'proj_id': proj.id,
            'url': pic_url
        })
    if len(pic_params) > 0:
        ProjPicMgr.batch_create(pic_params)

    # 新增操作记录
    __add_proj_op_log(operator_id, proj.id, proj_constant.PROJ_OP_TYPE_CREATE, "新建一个项目",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok')


def update_proj(operator_id, form):
    # 创建项目信息
    proj_params = {
        'proj_name': form.proj_name.data,
        'company_id': form.company_id.data,
        'address': form.address.data,
        'crew_num': form.crew_num.data,
        'description': form.description.data,
        'category': form.category.data
    }
    proj = ProjMgr.update_proj_by_id(form.proj_id.data, proj_params)
    if proj is None:
        return dict(status='error', msg='无效的项目编号')

    # 创建项目图片信息
    ProjPicMgr.clear_pic_list(proj.id)
    pic_url_list = form.pic_url_list.data.split(';')
    pic_params = []
    for pic_url in pic_url_list:
        pic_params.append({
            'proj_id': proj.id,
            'url': pic_url
        })
    if len(pic_params) > 0:
        ProjPicMgr.batch_create(pic_params)

    # 新增操作记录
    __add_proj_op_log(operator_id, proj.id, proj_constant.PROJ_OP_TYPE_UPDATE, "更改项目信息",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok')


def delete_proj(operator_id, proj_id):
    proj = ProjMgr.get(proj_id)
    if proj is None:
        return dict(status='error', msg='要删除的项目不存在')
    ProjMgr.delete(proj)
    ProjPicMgr.clear_pic_list(proj.id)
    # 新增操作记录
    __add_proj_op_log(operator_id, proj.id, proj_constant.PROJ_OP_TYPE_DELETE, "删除项目",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok')


def change_proj_status(operator_id, form):
    proj = ProjMgr.get(form.proj_id.data)
    proj_id = form.proj_id.data
    proj_status = form.proj_status.data
    from_status = proj.proj_status
    if proj is None:
        return dict(status='error', msg='要更改的项目不存在')
    ProjMgr.update(proj, proj_status=proj_status)

    __add_proj_op_log(operator_id, proj_id, proj_constant.PROJ_OP_TYPE_CHANGE_STATUS, '更改项目状态',
                      from_status=from_status, to_status=proj_status)

    return dict(status='ok')


def get_proj_list(page):
    order_by_list = [ProjMgr.model.id.desc()]
    expressions = [ProjMgr.model.is_del == 0]
    return page_util.get_page_result(ProjMgr.model, page=page,  expressions=expressions, page_size=10,
                                     filter_func=__proj_mapper, order_by_list=order_by_list)


def __proj_mapper(proj, biz_context):
    '''
    result:[{"company_id": 1, "company_name: "明星人力资源公司", "address": "浦东南路", "proj_name": "",
    "crew_num": 100, "description": "", "work_crew_num": 90, "current_month_income": 480001331, "message_count": 6}],
    :param proj:
    :return:
    '''

    item = dict()
    item['proj_id'] = proj.id
    item['company_id'] = proj.company_id
    item['company_name'] = __get_company_name_by_id(proj.company_id, biz_context)
    item['address'] = proj.address
    item['proj_name'] = proj.proj_name
    item['crew_num'] = proj.crew_num
    item['description'] = proj.description
    # TODO
    item['work_crew_num'] = 0
    item['current_month_income'] = 0
    item['message_count'] = 0
    return item


def __get_company_name_by_id(company_id, biz_context):
    company_data = biz_context['cache_data'].get('company', None)
    if company_data:
        return company_data[company_id].company_name if company_data.get(company_id) else ''

    company_data = dict()
    company_ids = list(set([item.company_id for item in biz_context['result_list']]))
    companies = CompanyMgr.get_companies_by_ids(company_ids)
    for company in companies:
        company_data = company
    biz_context['cache_data']['company'] = company_data
    return company_data[company_id].company_name if company_data.get(company_id) else ''


def __add_proj_op_log(operator_id, proj_id, op_type, memo, from_status, to_status):
    # 新增操作记录
    op_params = {
        'operator_id': operator_id,
        'proj_id': proj_id,
        'memo': memo,
        'op_type': op_type,
        'from_status': from_status,
        'to_status': to_status
    }
    ProjOpLogMgr.create(**op_params)


