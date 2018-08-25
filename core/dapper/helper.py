# -*- encoding: utf8 -*-

from flask import request
import codecs, os, struct, re, socket, random, ctypes, time
from core import app, log

__author__ = 'zhangchuan'

def to_hex(rid):
    """
    return hex of this number, but without '0x'

    :param rid:
    :return:
    """
    return hex(rid)[2:]

def current_mills():
    return round(time.time() * 1000, 0)

def current_microseconds():
    return round(time.time() * 1000000, 0)

def generate_random_id():
    return to_hex(build_time_id())

def build_urandom_id():
    random_id = codecs.encode(os.urandom(8), 'hex_codec').decode('utf-8')
    if random_id.startswith('0x') or random_id.startswith('-0x'):
        random_id = '{0:x}'.format(struct.unpack('Q', struct.pack('q', int(random_id, 16)))[0])
    random_id = random_id.zfill(16)
    return ctypes.c_long(int(random_id, 16)).value

def build_time_id():
    xx = int(time.time() * 1000000 * 1000)
    dal = codecs.encode(os.urandom(1), 'hex_codec').decode('utf-8')
    xx = (xx << 4) | (int(dal, 16) & 0x0F)
    return ctypes.c_long(xx).value

def is_health_url(url):
    if url.endswith('/health'):
        return True
    if 'heartBeat' in url or 'healthcheck' in url:
        return True
    return False

def is_path_in_blacklist(url):
    if url is None:
        return False
    blacklisted_paths = app.config.get('DAPPER_URL_BLACK_LIST', [])
    if len(blacklisted_paths) == 0:
        return False
    regexes = [re.compile(r) if isinstance(r, basestring) else r for r in blacklisted_paths]
    return any(r.match(url) for r in regexes)

def should_sampled(trace_id):
    tracing_percent = app.config.get('DAPPER_TRACE_PERCENT', 0)
    if tracing_percent == 0:
        return False
    ran = random.randint(0, tracing_percent - 1)
    return ran % tracing_percent == 0

def is_current_traced():
    return app.config.get('DAPPER_TRACE_SWITCH', False) \
           and not is_path_in_blacklist(request.path) \
           and getattr(request, 'is_sampled', '0') == '1'

def is_current_debug(req_headers, req_values=None, req_name=None):
    if not app.config.get('DAPPER_DEBUG_SWITCH', False):
        return False

    header_regexs = app.config.get('DAPPER_DEBUG_HEADER', {})
    if req_headers and len(header_regexs) > 0:
        for k, v in header_regexs:
            hea = req_headers.get(k, None)
            if hea and re.match(v, hea):
                return True

    value_regex = app.config.get('DAPPER_DEBUG_VALUE', {})
    if req_values and len(value_regex) > 0:
        for k, v in value_regex:
            hea = req_values.get(k, None)
            if hea and re.match(v, hea):
                return True

    url_regex = app.config.get('DAPPER_DEBUG_URL', [])
    if req_name and len(url_regex) > 0:
        for k in url_regex:
            if re.match(k, req_name):
                return True

    return False


def try_tracing(req_headers, req_name=None):
    if not app.config.get('DAPPER_TRACE_SWITCH', False):
        return None

    if is_path_in_blacklist(req_name):
        return None

    if req_headers.get('X-B3-Sampled', '0') == '1':
        trace_id = req_headers.get('X-B3-TraceId')
    else:
        trace_id = generate_random_id()
        if not should_sampled(trace_id):
            trace_id = None

    return trace_id


