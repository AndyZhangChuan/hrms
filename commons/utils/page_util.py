# -*- encoding: utf8 -*-
from core import app, db
import math
from sqlalchemy import func
from commons.utils import to_dict


def get_page_result(model, page=1, page_size=10, expressions=list(), order_by_list=list(), filter_func=None):
    result_list, total_page = __do_query(model, page, page_size, expressions, order_by_list)
    result = []
    for item in result_list:
        if filter_func is None:
            obj = to_dict(item)
        else:
            obj = filter_func(item, {'result_list': result_list, 'cache_data': {}})
        result.append(obj)

    data = {
        'status': 'ok',
        'content': {
            'result': result,
            'page': page,
            'total_page': total_page,
        }
    }
    return data


def __do_query(model, page=1, page_size=10, expressions=[], order_by_list=[]):
    count = db.session.query(func.count(model.id)).filter(*expressions).scalar()
    page_floor = int(math.ceil(count / page_size))
    total_page = page_floor if count % page_size == 0 else page_floor + 1

    page_query = db.session.query(model.id).filter(*expressions).order_by(model.id.desc())
    if page_size != 0:
        # 计算分页参数
        start = (page - 1) * page_size
        end = start + page_size
        page_query = page_query.slice(start, end)

    page_ids = [item[0] for item in page_query.all()]
    entities = model.query.filter(model.id.in_(page_ids)).order_by(*order_by_list)

    return entities, total_page
