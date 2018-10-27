# coding=utf-8
from commons.utils import page_util, to_dict
from data.manager import PluginMgr
from data.manager.proj import ProjMgr


def get_plugins(page, org_id):
    order_by_list = [ProjMgr.model.id.desc()]
    expressions = [ProjMgr.model.is_del == 0]
    if org_id > 0:
        expressions = [ProjMgr.model.org_id == org_id]
    return page_util.get_page_result(ProjMgr.model, page=page,  expressions=expressions, page_size=10,
                                     filter_func=__proj_plugins_mapper, order_by_list=order_by_list)


def update_proj_plugin(params):
    plugin = PluginMgr.query_first(filter_conditions={'module_type': params['module_type'], 'module_id': params['module_id'], 'plugin_id': params['plugin_id'], 'is_del': 0})
    if plugin:
        PluginMgr.update(plugin, props=params['props'])
    else:
        plugin = PluginMgr.create(**params)
    return to_dict(plugin)


def __proj_plugins_mapper(proj, biz_context):
    item = dict()
    item['proj_id'] = proj.id
    item['org_id'] = proj.org_id
    item['address'] = proj.address
    item['proj_name'] = proj.proj_name
    item['plugins'] = __get_plugins_by_proj_id(proj.org_id, proj.id)
    return item


def __get_plugins_by_proj_id(org_id, proj_id):
    plugins = PluginMgr.query({'org_id': org_id, 'proj_id': proj_id, 'is_del': 0})
    return to_dict(plugins)