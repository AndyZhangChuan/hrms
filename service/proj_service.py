# -*- encoding: utf8 -*-
from controller import get_request_org_id, get_request_proj_id
from data.manager import PicMgr
from data.manager.proj import ProjMgr, ProjOpLogMgr, ProjOfferMgr
from service.constant import proj_constant
from commons.utils import to_dict, web_util


def create_proj(form):

    org_id = get_request_org_id()
    proj = ProjMgr.create(org_id=org_id, **form)

    # 新增操作记录
    __add_proj_op_log(web_util.get_operator_id(), proj.id, proj_constant.PROJ_OP_TYPE_CREATE, "新建一个项目",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok', data=to_dict(proj))


def update_proj(proj_id, form):
    proj = ProjMgr.get(proj_id)
    if proj is None:
        return dict(status='error', msg='无效的项目编号')
    ProjMgr.update(proj, **form)
    # 新增操作记录
    __add_proj_op_log(web_util.get_operator_id(), proj.id, proj_constant.PROJ_OP_TYPE_UPDATE, "更改项目信息",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok', data=to_dict(proj))


def delete_proj(proj_id):
    proj = ProjMgr.get(proj_id)
    if proj is None:
        return dict(status='error', msg='要删除的项目不存在')
    ProjMgr.delete(proj)
    PicMgr.clear_pic_list(proj.id)
    # 新增操作记录
    __add_proj_op_log(web_util.get_operator_id(), proj.id, proj_constant.PROJ_OP_TYPE_DELETE, "删除项目",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok')


def change_proj_status(proj_id, status):
    proj = ProjMgr.get(proj_id)
    if proj is None:
        return dict(status='error', msg='要更改的项目不存在')
    from_status = proj.proj_status

    ProjMgr.update(proj, proj_status=status)

    __add_proj_op_log(web_util.get_operator_id(), proj_id, proj_constant.PROJ_OP_TYPE_CHANGE_STATUS, '更改项目状态',
                      from_status=from_status, to_status=status)

    return dict(status='ok')


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


def set_proj_tags(proj_id, tags):
    proj = ProjMgr.get(proj_id)
    if proj:
        ProjMgr.update(proj, tags=tags)


def create_offer(form):

    proj_id = get_request_proj_id()
    offer = ProjOfferMgr.create(proj_id=proj_id, **form)

    # 新增操作记录
    __add_proj_op_log(web_util.get_operator_id(), offer.id, proj_constant.PROJ_OP_TYPE_CREATE, "新建一个报价单",
                      0, 0)
    return dict(status='ok', data=to_dict(offer))


def update_offer(offer_id, form):
    offer = ProjOfferMgr.get(offer_id)
    if offer is None:
        return dict(status='error', msg='报价单不存在')
    ProjOfferMgr.update(offer, **form)
    # 新增操作记录
    __add_proj_op_log(web_util.get_operator_id(), offer.id, proj_constant.PROJ_OP_TYPE_UPDATE, "更改报价单信息",
                      0, 0)
    return dict(status='ok', data=to_dict(offer))
