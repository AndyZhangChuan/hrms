# -*- encoding: utf8 -*-
import requests
import time
from core import log


def http_request(url, params=None, method='get', timeout=1, is_json=True):

    begin_time = time.time()
    result = None
    try:
        r = None
        if method is 'get':
            if params is None:
                r = requests.get(url, timeout=timeout)
            else:
                r = requests.get(url, params=params, timeout=timeout)

        elif method is 'post':
            if params is None:
                r = requests.post(url, timeout=timeout)
            else:
                r = requests.post(url, data=params, timeout=timeout)

        if r is not None:
            if is_json is True:
                result = ('ok', r.status_code, r.json())
            else:
                result = ('ok', r.status_code, r.json())
        else:
            result = ('fail', '000', 'request failed')

    except requests.ConnectionError as e:
        log.info("[error_log] timeout - %s" % (url))
        result = ('fail', '000', 'request failed')

    except Exception, e:
        log.info("[error_log] error - %s, e=%s" % (url, e.message))
        result = ('fail', '000', 'request failed')

    finally:
        log.info("[time_log] %f - %s" % (time.time() - begin_time, url))
        return result
