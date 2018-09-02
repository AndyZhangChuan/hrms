# -*- encoding: utf8 -*-
from commons.exception import ValidationError
from hrms.plugins.plugin import Props

from flask import jsonify
from core import app
from inspect import getmembers, isclass
from hrms import plugins


@app.route("/plugins", methods=['POST', 'GET'])
def get_plugins():
    try:
        plugin_pool = {}
        members = getmembers(plugins)
        for member in members:
            if isclass(member[1]):
                plugin_pool[member[0]] = get_plugin_info(member[1])
        return jsonify(status='ok', content=plugin_pool)
    except ValidationError, e:
        return jsonify(status='fail', content=e.getMessage())


def get_plugin_info(plugin):
    id = plugin.__name__
    name = plugin.__plugin_name__
    desc = plugin.__desc__
    category = plugin.__category__
    priority = plugin.__priority__
    props = []
    members = getmembers(plugin)
    for member in members:
        if isinstance(member[1], Props):
            props.append({'type': member[1].type, 'default': member[1].default, 'nullable': member[1].nullable, 'name': member[0], 'comment': member[1].comment})
    props.sort(cmp=sort_props)
    return {'id': id, 'name': name, 'desc': desc, 'props': props, 'priority': priority, 'category': category}


def sort_props(a, b):
    """
    对props进行排序，timestamp类型的字段置顶，且start_time在end_time之前
    :param a
    :param b
    :return:
    """
    if a['type'] == 'timestamp' and b['type'] == 'timestamp':
        return cmp(len(b['name']), len(a['name']))
    elif a['type'] == 'timestamp':
        return -1
    elif b['type'] == 'timestamp':
        return 1
    return cmp(a['name'], b['name'])
