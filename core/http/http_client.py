# -*- encoding: utf8 -*-
import requests
from .intercept import XB3HTTPAdapter

__author__ = 'zhangchuan'


class HttpClient(object):
    def __init__(self, app_name):
        self.app_name = app_name
        self._session = requests.Session()
        xb3_http_adapter = XB3HTTPAdapter(app_name=app_name)
        self._session.mount('http://', xb3_http_adapter)
        self._session.mount('https://', xb3_http_adapter)

    def get(self, url, params=None, data=None, headers=None, timeout=None, **kwargs):
        return self._session.get(url, params=params, data=data, headers=headers, timeout=timeout, **kwargs)

    def post(self, url, params=None, data=None, headers=None, timeout=None, **kwargs):
        return self._session.post(url, params=None, data=data, headers=headers, timeout=timeout, **kwargs)

    def put(self, url, params=None, data=None, headers=None, timeout=None, **kwargs):
        return self._session.put(url, params=None, data=data, headers=headers, timeout=timeout, **kwargs)

    def delete(self, url, params=None, data=None, headers=None, timeout=None, **kwargs):
        return self._session.delete(url, params=None, data=data, headers=headers, timeout=timeout, **kwargs)
