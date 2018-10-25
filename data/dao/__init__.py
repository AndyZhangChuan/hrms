# coding=utf-8
from data.manager import DaoRelationMapMgr
from proj_dao import ProjDao
from fine_dao import FineDao
from crew_dao import CrewDao
from wage_dao import WageDao

dao_map = {
    'proj': ProjDao(),
    'fine': FineDao(),
    'crew': CrewDao(),
    'wage': WageDao(),
}

attrs = DaoRelationMapMgr.query({'is_del': 0})
attr_map = {
    item.dao + item.attr_name: item for item in attrs
}


def get(module, getter, attrs, filters):
    '''
    根据module执行对应的getter方法
    '''
    dao = dao_map[module]
    input_args = attr_map[module + getter].input_args
    args = {item: filters[item] for item in (input_args.split(',') if input_args else [])}
    data = getattr(dao, getter)(**args)
    for item in attrs:
        input_args = attr_map[module + item].input_args
        args = {item: filters[item] for item in (input_args.split(',') if input_args else [])}
        args['data'] = data
        getattr(dao, 'add_'+item)(**args)
    return data


def list(module, getter, attrs, filters):
    '''
    根据module执行对应的getter方法
    '''
    dao = dao_map[module]
    input_args = attr_map[module + getter].input_args
    args = {item: filters[item] if item in filters else None for item in (input_args.split(',') if input_args else [])}
    result = getattr(dao, getter)(**args)
    for data in result['datas']:
        for item in attrs:
            input_args = attr_map[module + item].input_args
            args = {item: filters[item] for item in (input_args.split(',') if input_args else [])}
            args['data'] = data
            getattr(dao, 'add_' + item)(**args)
    return result
