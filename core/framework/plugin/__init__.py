# coding=utf-8
import json
from inspect import getmembers

from core import plugin_pool
from commons.exception import ValidationError
from dao.models.proj import ProjPlugin
from plugins import Props


def execute_proj_plugin(proj_id, method, form, data):
    """
    执行给定商品包含的所有plugin逻辑
    :param proj_id: 项目编号
    :param method: plugin执行节点，如on_order_create, on_order_paid
    :param form: 输入表单
    :param data: 输入数据
    :return: 所有plugin逻辑执行完之后返回的数据
    """
    configs = ProjPlugin.query.filter_by(proj_id=proj_id, is_del=0).all()
    plugin_configs = [{'name': item.plugin_id, 'props': item.props} for item in configs]
    try:
        data = execute_plugin(plugin_configs, method, form, data)
    except ValidationError, e:
        return dict(status='error', msg=e.getMessage()['message'], trace=data['trace'])
    return dict(status='ok', data=data)


def execute_plugin(plugins, method, form, data):
    """
    执行plugin逻辑
    :param plugins: list，记录plugin name和props
    :param method: plugin执行节点，如on_order_create, on_order_paid
    :param form: 输入表单
    :param data: 输入数据
    :return: 所有plugin逻辑执行完之后返回的数据
    """

    # 记录插件执行记录
    data['trace'] = []

    # 从全局的插件池中获取产品对应的插件
    plugin_list = [{'object': plugin_pool[item['name']], 'props': item['props'], 'id': item['name']} for item in plugins]

    # 根据插件的priority排序
    sorted_plugin_list = sorted(plugin_list, key=lambda p : p['object'].__priority__, reverse=True)

    # 按顺序执行每一个插件对应的节点逻辑
    for plugin in sorted_plugin_list:
        if hasattr(plugin['object'], method):
            data['trace'].append(plugin['id'])
            props = {}
            if plugin['props']:
                props = json.loads(plugin['props'])
            props = init_props(plugin['object'], props)
            response = getattr(plugin['object'], method)(props, form, data)
            if response.status == 'ok':
                data = response.content
            elif response.status == 'return':
                raise ValidationError(response.message)
        else:
            continue
    return data


def init_props(plugin, props):
    members = getmembers(plugin)
    for member in members:
        if isinstance(member[1], Props):
            if member[0] not in props or props[member[0]] == '':
                props[member[0]] = member[1].default
            if member[1].type == 'float':
                props[member[0]] = float(props[member[0]])
            if member[1].type == 'int':
                props[member[0]] = int(props[member[0]])
    return props
