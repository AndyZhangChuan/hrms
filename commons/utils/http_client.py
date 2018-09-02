# -*- encoding: utf8 -*-
from commons.exception import NetWorkError
from commons.helper import concurrent_helper

import time
import traceback
import requests

REQUESTS_DATA_TYPE_JSON = 1
REQUESTS_DATA_TYPE_FORM = 2


def post(url, params=None, headers=None, data_type=REQUESTS_DATA_TYPE_FORM, timeout=5, retry_time=5, interval=0):
    kwargs = dict()
    kwargs['timeout'] = timeout
    kwargs['headers'] = headers if headers else {}
    if data_type == REQUESTS_DATA_TYPE_FORM:
        kwargs['data'] = params
    else:
        kwargs['json'] = params

    response = None
    for i in xrange(retry_time):
        try:
            response = requests.post(url, **kwargs)
            ret = response.json()
            return ret
        except Exception, ex:
            print "post send error.....msg=%s, url=%s, params=%s" % (ex.message, url, params)
            message_dict = dict(url=url, method='post', request=params, trace=traceback.format_exc())
            if response:
                message_dict['res_status_code'] = response.status_code
                message_dict['res_content'] = response.content
        if interval > 0:
            time.sleep(interval)
    raise NetWorkError("Connection error...")


def get(url, params=None, headers=None, timeout=None, retry_time=5, interval=0):
    headers = headers if headers else {}
    response = None
    for i in xrange(retry_time):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            ret = response.json()
            return ret
        except Exception, ex:
            print "get send error.....msg=%s, url=%s, params=%s" % (ex.message, url, params)
            message_dict = dict(url=url, method='get', request=params, trace=traceback.format_exc())
            if response:
                message_dict['res_status_code'] = response.status_code
                message_dict['res_content'] = response.content
        if interval > 0:
            time.sleep(interval)
    raise NetWorkError("Connection error...")


def concurrent_get(param_list, timeout=5, retry_time=5, interval=0):
    """
    并发发送get请求
    :param param_list: 参数字典列表, 格式为: [{url: '', params: {}, headers: {}}]
    :param timeout: 超时时间
    :param retry_time: 重试次数
    :param interval: 重试间隔时间
    :return:
    """
    new_params = pack_request_data(param_list, [timeout, retry_time, interval])
    try:
        return concurrent_helper.concurrent_execute_single_method(get, new_params)
    except Exception, ex:
        raise NetWorkError(ex.message)


def concurrent_post(param_list, data_type=REQUESTS_DATA_TYPE_FORM, timeout=5, retry_time=5, interval=0):
    """
    并发发送post请求
    :param param_list: 参数字典列表, 格式为: [{url: '', params: {}, headers: {}}]
    :param data_type: 参数格式, form/json
    :param timeout: 超时时间
    :param retry_time: 重试次数
    :param interval: 重试间隔
    :return:
    """
    new_params = pack_request_data(param_list, [data_type, timeout, retry_time, interval])
    try:
        return concurrent_helper.concurrent_execute_single_method(post, new_params)
    except Exception, ex:
        raise NetWorkError(ex.message)


def pack_request_data(require_params, other_params):
    result = []
    for param in require_params:
        item = list()
        item.append(param['url'])
        item.append(param.get('params', None))
        item.append(param.get('headers', None))
        item.extend(other_params)
        result.append(item)
    return result
