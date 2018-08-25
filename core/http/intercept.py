# -*- encoding: utf8 -*-

import time
from requests.adapters import HTTPAdapter
from ..utils import current_exception

__author__ = 'zhangchuan'


class XB3HTTPAdapter(HTTPAdapter):

    def __init__(self, app_name='0', *args, **kwargs):
        super(XB3HTTPAdapter, self).__init__(*args, **kwargs)
        self.app_name = app_name

    def send(self, *args, **kwargs):

        nreq = args[0]

        from ..dapper.local import HttpCallSpan
        span = HttpCallSpan()
        span.client_send(nreq)

        try:
            r = super(XB3HTTPAdapter, self).send(*args, **kwargs)
        except:
            span.client_receive(nreq, exception=current_exception())
            raise

        span.client_receive(nreq)

        return r

    def close(self):
        super(XB3HTTPAdapter, self).close()

    def add_headers(self, req, **kwargs):
        from ..dapper.local import LocalTrace
        from ..dapper.helper import current_mills
        req.headers.update(LocalTrace.to_dapper_headers(start_ts=current_mills()))
