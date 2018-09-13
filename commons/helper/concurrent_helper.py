# -*- coding: utf-8 -*-

from flask.globals import _request_ctx_stack
from concurrent import futures
from functools import partial
from hrms.commons.exception import ValidationError
from core import db

DEFAULT_WORKERS = 15
MAX_WORKERS = 20
CONCURRENT_EXECUTOR_THREAD = 0
CONCURRENT_EXECUTOR_PROCESS = 1


def concurrent_execute_single_method(method, params_list, customer_workers=DEFAULT_WORKERS,
                                     executor=CONCURRENT_EXECUTOR_THREAD, copy_request_ctx=False):
    """
    并发执行单个方法
    :param method: 方法名称
    :param params_list:参数二维列表
    :param customer_workers: 自定义线程数量
    :param executor: 执行器:  线程(默认), 进程
    :return:
    """
    workers = min(min(MAX_WORKERS, customer_workers), len(params_list))
    with pool_executor(executor)(workers) as executor:
        func = partial(make_future, method, request_ctx=_request_ctx_stack.top) if copy_request_ctx else \
               partial(make_future, method)
        res = executor.map(func(), *zip(*params_list))
    return list(res)


def concurrent_execute_multi_method(methods, params_list, customer_workers=DEFAULT_WORKERS,
                                    executor=CONCURRENT_EXECUTOR_THREAD):
    """
    并发执行多个方法
    :param methods: 方法列表
    :param params_list: 参数二维列表,与methods参数一一对应
    :param customer_workers:
    :param executor: 执行器:  线程(默认), 进程
    :return:
    """
    workers = min(min(MAX_WORKERS, customer_workers), max(len(methods), 1))
    if len(methods) != len(params_list):
        raise ValidationError("method quantity is inconsistent with parameter quantity")
    with pool_executor(executor)(workers) as executor:
        to_do = []
        for index, method in enumerate(methods):
            future = executor.submit(make_future(method, index), *params_list[index])
            to_do.append(future)

        result = [task.result() for task in futures.as_completed(to_do)]
        result = sorted(result, key=lambda x: x['index'])
        result = [x['data'] for x in result]

    if len(result) != len(methods):
        raise ValidationError('inconsistent result with methods')

    return result


def make_future(method, index=None, request_ctx=None):
    """
    An important caveat to this is that any operation relate to database must be MANUALLY committed, otherwise may result
    potential operation lost.
    """
    def future(*args, **kwargs):
        rv = _request_ctx_stack.push(request_ctx) if not _request_ctx_stack.top and request_ctx else None
        result = None
        try:
            result = method(*args, **kwargs)
        except Exception, ex:
            raise ex
        finally:
            if rv:
                _request_ctx_stack.pop()
            try:
                db.session.remove()
            except Exception, ex:
                print ex
        if index is None:
            return result
        else:
            return dict(index=index, data=result)
    return future


def pool_executor(executor):
    if executor == CONCURRENT_EXECUTOR_THREAD:
        return futures.ThreadPoolExecutor
    return futures.ProcessPoolExecutor




