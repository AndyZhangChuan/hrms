# -*- encoding: utf8 -*-

import time
from flask import request
from ..utils.json_utils import to_json
from ..utils.net_utils import local_ip_int, convert_ip_to_int

__author__ = 'zhangchuan'


class SpanContext(object):

    def __init__(self, first_span):
        self.first_span = first_span
        self.spans = []

    def add_span(self, cspan):
        cspan.trace_id = self.first_span.trace_id
        cspan.parent_span_id = self.first_span.span_id
        self.spans.append(cspan)

    def to_dict(self):
        return {'frist_span': self.first_span.to_dict(), 'spans': [s.to_dict() for s in self.spans]}

    def __repr__(self):
        return to_json(self.__dict__)

class Endpoint(object):

    def __init__(self, service_name, ipv4, port):
        self.service_name = service_name
        self.ipv4 = convert_ip_to_int(ipv4) if isinstance(ipv4, basestring) else int(ipv4)
        self.port = int(port)

    @classmethod
    def local_endpoint(cls, port):
        from core import get_app_name
        return Endpoint(get_app_name(), local_ip_int, port)

    @classmethod
    def request_endpoint(cls):
        from core import get_app_name
        port = int(str(request.host).split(':')[1]) if ':' in request.host else 80
        return Endpoint(get_app_name(), local_ip_int, port)

    def __repr__(self):
        return to_json(self.__dict__)

class Annotation(object):

    def __init__(self, a_key, a_timestamp, a_value=None, a_type=None):
        self.a_timestamp = a_timestamp
        self.a_type = a_type
        self.a_key = a_key
        self.a_value = a_value
        self.endpoint = None

    def set_endpint(self, endpoint):
        self.endpoint = endpoint
        return self

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return to_json(self.__dict__)

    @classmethod
    def client_send(cls, a_timestamp):
        """ The client sent ("cs") a request to a server
        @param a_timestamp:
        @return:
        """
        return Annotation('cs', a_timestamp, a_type=-1)

    @classmethod
    def client_receive(cls, a_timestamp):
        """ The client received ("cr") a response from a server
        @param a_timestamp:
        @return:
        """
        return Annotation('cr', a_timestamp, a_type=-1)

    @classmethod
    def server_receive(cls, a_timestamp):
        """ The server received ("sr") a request from a client
        @param a_timestamp:
        @return:
        """
        return Annotation('sr', a_timestamp, a_type=-1)

    @classmethod
    def server_send(cls, a_timestamp):
        """ The server sent ("ss") a response to a client.
        @param a_timestamp:
        @return:
        """
        return Annotation('ss', a_timestamp, a_type=-1)

    @classmethod
    def http_path(cls, a_timestamp, http_path):
        return Annotation('http.path', a_timestamp, http_path, a_type=6)

    @classmethod
    def http_status(cls, a_timestamp, status_code):
        return Annotation('http.status', a_timestamp, status_code, a_type=6)

    @classmethod
    def http_error(cls, a_timestamp, error_info):
        if len(error_info) > 1024:
            error_info = error_info[:1024]
        return Annotation('http.error', a_timestamp, error_info, a_type=6)

class Span(object):

    def __init__(self, trace_id, span_id, parent_span_id, name, initiator=0):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.name = name
        self.initiator = initiator

        self.start_ts = 0
        self.end_ts = 0
        self.duration = 0
        self.annos = []
        self.endpoint = None

    def add_anno(self, anno):
        self.annos.append(anno)

    def start(self, endpoint=None):
        self.start_ts = round(time.time() * 1000000)

        if self.initiator == 1:
            an = Annotation.client_send(self.start_ts)
        else:
            an = Annotation.server_receive(self.start_ts)

        if endpoint:
            an.set_endpint(endpoint)
            self.endpoint = endpoint

        self.annos.append(an)

    def end(self, endpoint=None):
        end_ts = round(time.time() * 1000000)
        self.end_ts = end_ts
        self.duration = end_ts - self.start_ts

        if self.initiator == 1:
            an = Annotation.client_receive(end_ts)
        else:
            an = Annotation.server_send(end_ts)

        if endpoint:
            an.set_endpint(endpoint)
            self.endpoint = endpoint
        elif self.endpoint:
            an.set_endpint(endpoint)
        else:
            self.endpoint = Endpoint.request_endpoint()

        self.annos.append(an)

    def to_dict(self):
        return dict(self.__dict__).update()

    def __repr__(self):
        return to_json(self.__dict__)

if __name__ == '__main__':
    spanx = Span()
    print to_json(spanx.__dict__)








