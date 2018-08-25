# -*- encoding: utf8 -*-

from helper import generate_random_id, current_microseconds
import time

__author__ = 'zhangchuan'


class Type(object):

    def __init__(self, value, text):
        self.value = value
        self.text = text


class Types(object):

    BOOL = Type(0, 'BOOL')
    BYTES = Type(1, 'BYTES')
    I16 = Type(0, 'I16')
    I32 = Type(0, 'I32')
    I64 = Type(0, 'I64')
    DOUBLE = Type(0, 'DOUBLE')
    STRING = Type(0, 'STRING')

    def __init__(self):
        pass

class BeanFactory(object):

    def __init__(self):
        pass

    @classmethod
    def create_span(cls, trace_id, span_name, parent_id=None):
        assert trace_id and len(trace_id) > 0, "trace_id of span can not be empty"
        assert span_name and len(span_name) > 0, "span_name can not be empty"
        return Span(trace_id, span_name, generate_random_id(), parent_id, current_microseconds(), 0)

    @classmethod
    def create_client_send_anno(cls, endpoint):
        return cls.create_annotation(Constants.CLIENT_SEND, endpoint)

    @classmethod
    def create_client_receive_anno(cls, endpoint):
        return cls.create_annotation(Constants.CLIENT_RECV, endpoint)

    @classmethod
    def create_server_receive_anno(cls, endpoint):
        return cls.create_annotation(Constants.SERVER_RECV, endpoint)

    @classmethod
    def create_server_send_anno(cls, endpoint):
        return cls.create_annotation(Constants.SERVER_SEND, endpoint)

    @classmethod
    def create_annotation(cls, value, endpoint):
        assert value and len(value) > 0, "value of annotation can not be empty"
        assert endpoint, "endpoint of annotation can not be empty"
        return Annotation(value, current_microseconds(), endpoint)

    @classmethod
    def create_binary_anno(cls, key, value, endpoint, value_type=Types.STRING):
        assert key and len(key) > 0, "key of binary annotation can not be empty"
        assert value is not None, "value of binary annotation can not be empty"
        assert endpoint, "endpoint of binary annotation can not be empty"
        return BinaryAnnotation(key, value, endpoint=endpoint, value_type=value_type)

    @classmethod
    def create_http_path_binary(cls, http_path, endpoint):
        return BeanFactory.create_binary_anno(TraceKeys.HTTP_PATH, http_path, endpoint)

    @classmethod
    def create_http_url_binary(cls, http_url, endpoint):
        return BeanFactory.create_binary_anno(TraceKeys.HTTP_URL, http_url, endpoint)

    @classmethod
    def create_status_code_binary(cls, status_code, endpoint):
        return BeanFactory.create_binary_anno(TraceKeys.HTTP_STATUS_CODE, status_code, endpoint)

    @classmethod
    def create_http_method_binary(cls, http_method, endpoint):
        return BeanFactory.create_binary_anno(TraceKeys.HTTP_METHOD, http_method, endpoint)

    @classmethod
    def create_endpoint(cls, service_name, ipv4, port):
        return Endpoint(service_name=service_name, ipv4=ipv4, port=port)


class Span(object):

    def __init__(self, trace_id=0, name="", id=0, parent_id=None, timestamp=0, duration=0):
        self.traceIdHigh = 0
        self.traceId = trace_id
        self.name = name
        self.id = id
        self.parentId = parent_id
        self.timestamp = timestamp
        self.duration = duration
        self.annotations = []
        self.binaryAnnotations = []

    def add_annotation(self, anno):
        self.annotations.append(anno)

    def add_binary(self, anno):
        self.binaryAnnotations.append(anno)

    def fill_delta(self, delta_mills):
        if delta_mills > 1:
            self.timestamp += delta_mills

    def has_error_binary(self):
        for binary in self.binaryAnnotations:
            if binary.key == TraceKeys.ERROR:
                return True
        return False

    def end(self):
        """
        calc duration between start mills and end mills

        :return:
        """
        self.duration = current_microseconds() - self.timestamp

class Endpoint(object):

    def __init__(self, service_name="", ipv4=0, ipv6="", port=0):
        self.serviceName = service_name
        self.ipv4 = ipv4
        self.ipv6 = ipv6  # byte[]
        self.port = port

class Annotation(object):

    def __init__(self, value="", timestamp=0, endpoint=None):
        self.value = value
        self.timestamp = timestamp
        self.endpoint = endpoint

class BinaryAnnotation(object):

    def __init__(self, key="", value=None, value_type=Types.STRING, endpoint=None):
        self.key = key
        self.value = value  # byte[]
        self.type = value_type.text
        self.endpoint = endpoint


class TraceKeys(object):

    HTTP_HOST = "http.host"
    HTTP_METHOD = "http.method"
    HTTP_PATH = "http.path"
    HTTP_URL = "http.url"
    HTTP_STATUS_CODE = "http.status_code"
    HTTP_REQUEST_SIZE = "http.request.size"
    HTTP_RESPONSE_SIZE = "http.response.size"

    JDBC_URL = "jdbc.url"
    STATEMENT_SQL = "statement.sql"
    STATEMENT_PARAMETER = "statement.parameter"
    STATEMENT_ROWCOUNT = "statement.rowcount"

    REDIS_COMMAND = "redis.command"
    REDIS_URL = "redis.url"
    COMMAND_PARAMETER = "command.parameter"

    RPC_HTTP = "http.call"
    RPC_HTTP_HOST = "rpc.http.host"
    RPC_HTTP_PORT = "rpc.http.port"
    RPC_HTTP_PATH = "rpc.http.path"
    RPC_HTTP_URL = "rpc.http.url"
    RPC_HTTP_METHOD = "rpc.http.method"

    CELERY_TASK_NAME = "celery.task.name"
    CELERY_TASK_ID = "celery.task.id"
    CELERY_EXCHANGE = "celery.exchange"
    CELERY_ROUTING_KEY = "celery.routing.key"
    CELERY_TASK_STATE = "celery.task.state"
    CELERY_TASK_PARAMETER = "celery.task.parameter"

    ERROR = "error"

    def __init__(self):
        pass

class Constants(object):

    CLIENT_SEND = "cs"
    CLIENT_RECV = "cr"

    SERVER_SEND = "ss"
    SERVER_RECV = "sr"

    WIRE_SEND = "ws"
    WIRE_RECV = "wr"

    CLIENT_SEND_FRAGMENT = "csf"
    CLIENT_RECV_FRAGMENT = "crf"

    SERVER_SEND_FRAGMENT = "ssf"
    SERVER_RECV_FRAGMENT = "srf"

    LOCAL_COMPONENT = "lc"

    CLIENT_ADDR = "ca"
    SERVER_ADDR = "sa"

    DAPPER_HEADERS = "dapper_headers"

    def __init__(self):
        pass

class B3HeaderNames(object):

    TRACE_ID = 'X-B3-TraceId'
    PARENT_SPAN_ID = 'X-B3-ParentSpanId'
    SAMPLED = 'X-B3-Sampled'
    FLAG = 'X-B3-Flag'
    START_TS = 'X-B3-StartTs'

    def __init__(self):
        pass

if __name__ == '__main__':
    print time.time()
    print time.time() * 1000000


