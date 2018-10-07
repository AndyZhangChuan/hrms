# -*- encoding: utf8 -*-
from flask import request

from core.framework.plugin import execute_proj_plugin
from dao.manager.proj import ProjMgr, ProjPluginMgr, ProjPicMgr, ProjOpLogMgr, ProjRichTextMgr
from service.constant import proj_constant
from service.constant import proj_nodes
from commons.utils import page_util, time_util
from commons.utils import to_dict
import time


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
        'wage_range': form.wage_range.data,
        'tags': form.tags.data,
        'category': form.category.data
    }
    proj = ProjMgr.update_proj_by_id(form.id.data, proj_params)
    if proj is None:
        return dict(status='error', msg='无效的项目编号')
    # 新增操作记录
    __add_proj_op_log(operator_id, proj.id, proj_constant.PROJ_OP_TYPE_UPDATE, "更改项目信息",
                      proj.proj_status, proj.proj_status)
    return dict(status='ok', content=__proj_mapper(proj, None))


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

    params = {'proj_status': proj_status}
    if proj_status == proj_constant.PROJ_STATUS_WORKING:
        params['start_time'] = int(time.time())
    elif proj_status == proj_constant.PROJ_STATUS_END:
        params['end_time'] = int(time.time())

    ProjMgr.update(proj, **params)

    __add_proj_op_log(operator_id, proj_id, proj_constant.PROJ_OP_TYPE_CHANGE_STATUS, '更改项目状态',
                      from_status=from_status, to_status=proj_status)

    return dict(status='ok')


def get_proj_list(company_id, page):
    order_by_list = [ProjMgr.model.id.desc()]
    expressions = [ProjMgr.model.company_id == company_id, ProjMgr.model.is_del == 0]
    return page_util.get_page_result(ProjMgr.model, page=page,  expressions=expressions, page_size=10,
                                     filter_func=__proj_mapper, order_by_list=order_by_list)


def get_proj_plugins_by_company(page, company_id):
    order_by_list = [ProjMgr.model.id.desc()]
    expressions = [ProjMgr.model.is_del == 0, ProjMgr.model.company_id == company_id]
    return page_util.get_page_result(ProjMgr.model, page=page,  expressions=expressions, page_size=10,
                                     filter_func=__proj_plugins_mapper, order_by_list=order_by_list)


def update_proj_plugin(params):
    plugin = ProjPluginMgr.query_first(filter_conditions={'proj_id': params['proj_id'], 'plugin_id': params['plugin_id'], 'is_del': 0})
    if plugin:
        if params['is_del'] == 0:
            ProjPluginMgr.update(plugin, props=params['props'])
        else:
            ProjPluginMgr.delete(plugin)
    else:
        ProjPluginMgr.create(proj_id=params['proj_id'], plugin_name=params['plugin_name'], plugin_id=params['plugin_id'], props=params['props'])

    return to_dict(ProjPluginMgr.query(filter_conditions={'proj_id': params['proj_id'], 'is_del': 0}))


def __proj_mapper(proj, biz_context):
    '''
    result:[{"company_id": 1, "address": "浦东南路", "proj_name": "",
    "crew_num": 100, "description": "", "work_crew_num": 90, "current_month_income": 480001331, "message_count": 6}],
    :param proj:
    :return:
    '''
    proj_dict = to_dict(proj)
    logo_pic = ProjPicMgr.get_img_by_type(proj.id, 'logo')
    proj_dict['logo_url'] = logo_pic[0].url if len(logo_pic) else ''
    intro_pic_list = ProjPicMgr.get_img_by_type(proj.id, 'intro')
    proj_dict['intro_pic_list'] = []
    for item in intro_pic_list:
        proj_dict['intro_pic_list'].append({'url': item.url, 'id': item.id})
    proj_dict['highlight_tag'] = get_proj_highlight_title(proj.id)
    proj_dict['update_time'] = proj_dict['update_time'].strftime("%Y-%m-%d")
    return proj_dict


def __proj_plugins_mapper(proj, biz_context):
    '''
    result:[{"company_id": 1, "address": "浦东南路", "proj_name": "",
    "crew_num": 100, "description": "", "work_crew_num": 90, "current_month_income": 480001331, "message_count": 6}],
    :param proj:
    :return:
    '''

    item = dict()
    item['proj_id'] = proj.id
    item['company_id'] = proj.company_id
    item['address'] = proj.address
    item['proj_name'] = proj.proj_name
    item['crew_num'] = proj.crew_num
    item['wage_range'] = proj.wage_range
    item['plugins'] = __get_plugins_by_proj_id(proj.id)
    return item


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


def __get_plugins_by_proj_id(proj_id):
    plugins = ProjPluginMgr.query({'proj_id': proj_id, 'is_del': 0})
    return to_dict(plugins)


def set_proj_tags(proj_id, tags):
    proj = ProjMgr.get(proj_id)
    if proj:
        ProjMgr.update(proj, tags=tags)


def create_or_update_proj_rich_text(proj_id, title, text_type, content, sequence=0, subtitle='', rich_text_id=0):
    if rich_text_id:
        rich_text = ProjRichTextMgr.get(rich_text_id)
        ProjRichTextMgr.update(rich_text, title=title, sequence=sequence, rich_text=content, subtitle=subtitle)
    else:
        sequence = ProjRichTextMgr.get_last_sequence_by_type(proj_id, text_type) + 1
        rich_text = ProjRichTextMgr.create(proj_id=proj_id, title=title, text_type=text_type, sequence=sequence, rich_text=content, subtitle=subtitle)
    return to_dict(rich_text)


def delete_proj_rich_text(rich_text_id):
    rich_text = ProjRichTextMgr.get(rich_text_id)
    if rich_text:
        ProjRichTextMgr.delete(rich_text)


def create_proj_pic(proj_id, img_type, url, override=False):
    if override:
        ProjPicMgr.clear_pic_list(proj_id, img_type)
        sequence = 1
    else:
        sequence = ProjPicMgr.get_last_sequence_by_type(proj_id, img_type) + 1
    return ProjPicMgr.create(proj_id=proj_id, img_type=img_type, url=url, sequence=sequence)


def delete_proj_pic(pic_id):
    pic = ProjPicMgr.get(pic_id)
    if pic:
        ProjPicMgr.delete(pic)


def get_proj_base_info(proj_id):
    proj = ProjMgr.get(proj_id)
    if proj:
        return __proj_mapper(proj, None)
    else:
        return None


def get_proj_detail(proj_id):
    rich_text_list = ProjRichTextMgr.get_richtext_by_type(proj_id, 'proj_recruit_detail')
    result = []
    for item in rich_text_list:
        rich_text = to_dict(item)
        intro_pic_list = ProjPicMgr.get_img_by_type(proj_id, item.title)
        rich_text['pic_list'] = []
        for pic in intro_pic_list:
            rich_text['pic_list'].append({'url': pic.url, 'id': pic.id})
        result.append(rich_text)
    return result


def get_proj_highlight(proj_id):
    rich_text = ProjRichTextMgr.query_first({'proj_id': proj_id, 'text_type': 'proj_highlight'},
                                      order_list=[ProjRichTextMgr.model.sequence.desc()])
    if not rich_text:
        return None
    rich_text = to_dict(rich_text)
    intro_pic_list = ProjPicMgr.query({'proj_id': proj_id, 'img_type': 'proj_highlight'},
                                      order_list=[ProjPicMgr.model.sequence.desc()])
    rich_text['pic_list'] = []
    for pic in intro_pic_list:
        rich_text['pic_list'].append({'url': pic.url, 'sequence': pic.sequence})
    return rich_text


def get_proj_highlight_title(proj_id):
    rich_text = ProjRichTextMgr.query_first({'proj_id': proj_id, 'text_type': 'proj_highlight'})
    return rich_text.title if rich_text else None
