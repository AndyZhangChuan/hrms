# -*- encoding: utf8 -*-

import json, random, threading, re

from helper import generate_random_id, current_mills
from model import BeanFactory, TraceKeys, Constants, B3HeaderNames, Types
from ..utils.net_utils import local_ip_int, convert_ip_to_int
from ..utils.json_utils import to_json_no_tab
from ..utils import current_exception
from ..log import getLogger

__author__ = 'zhangying'

log = getLogger(__name__)

topic_dapper_name = 'topic_dapper_trace_new'

_trace_local = threading.local()


class TraceBean(object):

    def __init__(self, service_name, traced_id=None, parent_span_id=None, start_ts=0, sample=0, flag=0):
        self.service_name = service_name
        self.trace_id = traced_id
        # log.info("self.trace_id is %s" % self.trace_id)
        self.parent_span_id = parent_span_id
        # log.info("self.parent_span_id is %s" % self.parent_span_id)
        self.start_ts = start_ts
        self.debug = True if int(flag) == 1 else False
        self.sampled = True if int(sample) == 1 else False
        # log.info("self.sampled is %s" % self.sampled)
        self.spans = []
        self.span_map = {}
        self.last_span_id = parent_span_id
        self.delta_mills = start_ts - current_mills() if int(start_ts) > 0 else 0
        # log.info("self.last_span_id is %s" % self.last_span_id)

class LocalTrace(object):

    def __init__(self):
        pass

    @classmethod
    def current_context(cls):
        return getattr(_trace_local, 'trace_bean', None)

    @classmethod
    def set_context(cls, trace_bean):
        setattr(_trace_local, 'trace_bean', trace_bean)

    @classmethod
    def clear_context(cls):
        delattr(_trace_local, 'trace_bean')

    @classmethod
    def sampled(cls):
        return cls.current_context() and getattr(_trace_local.trace_bean, 'sampled', False)

    @classmethod
    def trace_id(cls):
        return cls.current_context() and getattr(_trace_local.trace_bean, 'trace_id', None)

    @classmethod
    def parent_span_id(cls):
        return cls.current_context() and getattr(_trace_local.trace_bean, 'parent_span_id', None)

    @classmethod
    def debug(cls):
        return cls.current_context() and getattr(_trace_local.trace_bean, 'debug', 0)

    @classmethod
    def last_span_id(cls):
        return cls.current_context() and getattr(_trace_local.trace_bean, 'last_span_id', None)

    @classmethod
    def set_last_span_id(cls, last_span_id):
        if cls.current_context():
            setattr(_trace_local.trace_bean, 'last_span_id', last_span_id)

    @classmethod
    def append_span(cls, span):
        cls.spans().append(span)

    @classmethod
    def spans(cls):
        if cls.current_context():
            return getattr(_trace_local.trace_bean, 'spans', [])
        return []

    @classmethod
    def to_dapper_headers(cls, start_ts=0):
        headers = {B3HeaderNames.SAMPLED: 1 if cls.sampled() else 0}
        if cls.sampled():
            headers[B3HeaderNames.TRACE_ID] = cls.trace_id()
            headers[B3HeaderNames.PARENT_SPAN_ID] = cls.last_span_id()
            headers[B3HeaderNames.FLAG] = 1 if cls.debug() else 0
            headers[B3HeaderNames.START_TS] = start_ts
        return headers

    @classmethod
    def headers_to_bean(cls, service_name, headers):
        # service_name, traced_id=None, parent_span_id=None, start_ts=None, sample=0, flag=0):
        return TraceBean(service_name, headers.get(B3HeaderNames.TRACE_ID, None),
                         headers.get(B3HeaderNames.PARENT_SPAN_ID, None),
                         headers.get(B3HeaderNames.START_TS, None),
                         headers.get(B3HeaderNames.SAMPLED, 0),
                         headers.get(B3HeaderNames.FLAG, 0))

empty = TraceBean("")

class DapperLocal(object):

    service_name = None
    freeKafkaLogger = None
    app_config = None

    def __init__(self, service_name, free_kafka_logger, app_config):
        DapperLocal.service_name = service_name
        DapperLocal.freeKafkaLogger = free_kafka_logger
        DapperLocal.app_config = app_config

    @classmethod
    def start(cls, context, trace_identifier):
        """
        every request's trace from here
        """
        try:
            if not cls.trace_switch():
                return
            sampled = context.sampled
            if not sampled and cls.enable_self_trace():
                sampled = cls.dice(trace_identifier)

            context = TraceBean(context.service_name, traced_id=context.trace_id,
                                parent_span_id=context.parent_span_id, start_ts=context.start_ts)
            if sampled:
                context.sampled = True
            if not context.trace_id:
                context.trace_id = generate_random_id()

            LocalTrace.set_context(context)
        except:
            log.error("dapper start error: %s" % current_exception())

    @classmethod
    def end(cls):
        """
        every request end here
        """
        try:
            if not cls.trace_switch():
                return

            context = LocalTrace.current_context()
            if not context:
                return
            LocalTrace.clear_context()
        except:
            log.error("dapper end error: %s" % current_exception())

    @classmethod
    def dice(cls, request_identifier):
        """
        global_probability means 1/global_probability,
        for example: 50 - means 1/50

        :param request_identifier:
        :return:
        """
        if not request_identifier:
            return False
        probability = cls.sample_percent()
        probabilities = cls.identifier_percent()
        if probabilities and probabilities in probabilities:
            probability = probabilities.get(request_identifier, 0)

        if probability == 0:
            return False

        ran = random.randint(0, probability - 1)
        return ran % probability == 0

    @classmethod
    def _context_has_error(cls, context):
        for span in context.spans:
            if span and span.has_error_binary:
                return True
        return False

    @classmethod
    def trace_switch(cls):
        return cls.app_config and cls.app_config.get('DAPPER_TRACE_SWITCH', False)

    @classmethod
    def enable_self_trace(cls):
        return cls.app_config and cls.app_config.get('DAPPER_SELF_SAMPLE', False)

    @classmethod
    def sample_percent(cls):
        if cls.app_config:
            return cls.app_config.get('DAPPER_TRACE_PERCENT', 0)
        return 0

    @classmethod
    def identifier_percent(cls):
        if cls.app_config:
            return cls.app_config.get('DAPPER_URL_PERCENT', {})
        return {}



class ComponentSpan(object):

    def __init__(self, span_name, endpoint):
        try:
            if not DapperLocal.trace_switch():
                return
            self.span = None
            self.set_span(span_name)
            self.endpoint = endpoint
        except:
            log.error("ComponentSpan error: %s" % current_exception())

    def set_span(self, span_name):
        if DapperLocal.trace_switch() and span_name:
            self.span = BeanFactory.create_span(LocalTrace.trace_id(), span_name, LocalTrace.last_span_id())
            LocalTrace.set_last_span_id(self.span.id)

    def set_endpoint(self, ipv4=None, port=0):
        self.endpoint = BeanFactory.create_endpoint(DapperLocal.service_name, ipv4, port)

    def add_binary(self, key, value, value_type=Types.STRING):
        self.span.add_binary(BeanFactory.create_binary_anno(key, value, endpoint=self.endpoint, value_type=value_type))

    def add_annotation(self, value):
        self.span.add_annotation(BeanFactory.create_annotation(value, self.endpoint))

    def start(self):
        pass

    def end(self, logging=False):
        self.span.end()
        # hold util dapper end
        LocalTrace.append_span(self.span)
        return self

    def client_send(self, *args, **kwargs):
        try:
            if not DapperLocal.trace_switch():
                return
            self._client_send(*args, **kwargs)
        except:
            log.error("client_send error: %s" + current_exception())

    def client_receive(self, *args, **kwargs):
        try:
            if not DapperLocal.trace_switch():
                return
            self._client_receive(*args, **kwargs)
            self.end(logging=True)
        except:
            log.error("client_receive error: %s" + current_exception())

    def server_receive(self, *args, **kwargs):
        try:
            if not DapperLocal.trace_switch():
                return
            self._server_receive(*args, **kwargs)
        except:
            log.error("server_receive error: %s" + current_exception())

    def server_send(self, *args, **kwargs):
        try:
            if not DapperLocal.trace_switch():
                return
            self._server_send(*args, **kwargs)
            self.end(logging=True)
        except:
            log.error("server_receive error: %s" + current_exception())

    # implement following methods
    def _client_send(self, *args, **kwargs):
        raise RuntimeError("must implement this method is subclass %s " % self)

    def _client_receive(self, *args, **kwargs):
        raise RuntimeError("must implement this method is subclass %s " % self)

    def _server_receive(self, *args, **kwargs):
        raise RuntimeError("must implement this method is subclass %s " % self)

    def _server_send(self, *args, **kwargs):
        raise RuntimeError("must implement this method is subclass %s " % self)


class FlaskRequestSpan(ComponentSpan):

    def __init__(self):
        from flask import request
        port = int(str(request.host).split(':')[1]) if ':' in request.host else 80
        endpoint = BeanFactory.create_endpoint(DapperLocal.service_name, local_ip_int, port)
        super(FlaskRequestSpan, self).__init__("%s %s" % (request.method, request.path), endpoint=endpoint)

    def _server_receive(self, *args, **kwargs):
        self.add_annotation(Constants.SERVER_RECV)

    def _server_send(self, *args, **kwargs):
        from flask import request
        self.add_annotation(Constants.SERVER_SEND)
        self.add_binary(TraceKeys.HTTP_PATH, request.path)
        self.add_binary(TraceKeys.HTTP_STATUS_CODE, str(getattr(request, 'response_status_code', 200)))
        self.add_binary(TraceKeys.HTTP_URL, request.url)

        self.end(logging=True)

class SqlAlchemySpan(ComponentSpan):

    def __init__(self, span_name, ipv4=None, port=3306):
        endpoint = BeanFactory.create_endpoint(DapperLocal.service_name, ipv4 if ipv4 else local_ip_int, port)
        super(SqlAlchemySpan, self).__init__(span_name, endpoint=endpoint)

    def _client_send(self, conn, cursor, statement, parameters, context, executemany):
        self.add_annotation(Constants.CLIENT_SEND)

    def _client_receive(self, conn, cursor, statement, parameters, context, executemany):
        engine_url = conn.engine.url
        port = engine_url.port if engine_url.port else 3306
        jdbc_url = "%s:%s/%s" % (engine_url.host, port, engine_url.database)

        self.add_annotation(Constants.CLIENT_RECV)
        self.add_binary(TraceKeys.JDBC_URL, jdbc_url)
        self.add_binary(TraceKeys.STATEMENT_PARAMETER, to_json_no_tab(parameters))
        self.add_binary(TraceKeys.STATEMENT_ROWCOUNT, str(cursor.rowcount if cursor.rowcount else 0))
        self.add_binary(TraceKeys.STATEMENT_SQL, statement)

    @classmethod
    def my_on_connect(cls, db_conn, conn_record):
        # engine_url = db_conn.engine.url
        # port = engine_url.port if engine_url.port else 3306
        # name = "mysql connect"
        # component = SqlAlchemySpan(name, ipv4=convert_ip_to_int(engine_url.host), port=port)
        # component.end(logging=True)
        # log.debug("New db connect conn is %s" % db_conn)
        pass

    @classmethod
    def before_cursor_execute(cls, conn, cursor, statement, parameters, context, executemany):
        if not DapperLocal.trace_switch():
            return
        # log.debug("before_cursor_execute triggered")
        engine_url = conn.engine.url
        port = engine_url.port if engine_url.port else 3306
        if context.isddl:
            opt = 'create'
        elif context.isdelete:
            opt = 'delete'
        elif context.isinsert:
            opt = 'insert'
        else:
            opt = 'select'
        name = "mysql %s" % opt
        span = SqlAlchemySpan(name, ipv4=convert_ip_to_int(engine_url.host), port=port)
        span.client_send(conn, cursor, statement, parameters, context, executemany)
        context.span = span

    @classmethod
    def after_cursor_execute(cls, conn, cursor, statement, parameters, context, executemany):
        if not DapperLocal.trace_switch():
            return
        # log.debug("after_cursor_execute triggered")
        span = context.span
        span.client_receive(conn, cursor, statement, parameters, context, executemany)
        delattr(context, 'span')

    @classmethod
    def add_listen_hooks(cls):
        from sqlalchemy.event import listen
        from sqlalchemy.pool import Pool
        from sqlalchemy.engine import Engine

        listen(Pool, 'connect', cls.my_on_connect)
        listen(Engine, "before_cursor_execute", cls.before_cursor_execute)
        listen(Engine, 'after_cursor_execute', cls.after_cursor_execute)

class RedisSpan(ComponentSpan):

    def __init__(self):
        super(RedisSpan, self).__init__(None, None)

    def _client_send(self, command, conn, retried):
        # log.debug("RedisSpan client_send")
        name = "redis %s" % str(command).lower()
        if retried:
            name += " retry"
        self.set_span(name)
        self.set_endpoint(convert_ip_to_int(conn.host), conn.port)
        self.add_annotation(Constants.CLIENT_SEND)

    def _client_receive(self, command, conn, params_tuple, result, exception=None):
        # log.debug("RedisSpan client_receive")
        server_url = "%s:%s/%s" % (conn.host, conn.port, conn.db)
        self.add_annotation(Constants.CLIENT_RECV)
        self.add_binary(TraceKeys.REDIS_URL, server_url)
        self.add_binary(TraceKeys.REDIS_COMMAND, command)
        self.add_binary(TraceKeys.COMMAND_PARAMETER, to_json_no_tab(params_tuple))
        if exception:
            self.add_binary(TraceKeys.ERROR, 'redis command error: %s' % exception)

host_port_patt = re.compile('//([\w.]+):?([\d]+)?')

class HttpCallSpan(ComponentSpan):

    def __init__(self):
        super(HttpCallSpan, self).__init__(None, None)

    def _client_send(self, http_request):
        mat = host_port_patt.findall(http_request.url)
        host = mat[0][0]
        port = mat[0][1] if mat[0][1] else 80
        if not re.match('\d+.\d+.\d+.\d+', host):
            host = "8.8.8.8"
        name = "rpc http %s" % http_request.method
        self.set_span(name)
        self.set_endpoint(convert_ip_to_int(host), port)
        self.add_annotation(Constants.CLIENT_SEND)
        self.add_binary(TraceKeys.RPC_HTTP_HOST, host)
        # self.add_binary(TraceKeys.RPC_HTTP_PORT, port)

    def _client_receive(self, http_request, exception=None):
        self.add_annotation(Constants.CLIENT_RECV)
        path = http_request.url
        if '?' in path:
            path = path[0:path.index('?')]
        self.add_binary(TraceKeys.RPC_HTTP_PATH, path)
        self.add_binary(TraceKeys.RPC_HTTP_URL, http_request.path_url)
        self.add_binary(TraceKeys.RPC_HTTP_METHOD, http_request.method)
        if exception:
            self.add_binary(TraceKeys.ERROR, 'http call error: %s' % exception)

class CeleryTaskSpan(ComponentSpan):

    dapper_local = None

    def __init__(self):
        super(CeleryTaskSpan, self).__init__(None, None)

    @classmethod
    def before_task_publish(cls, body, exchange, routing_key, headers, properties, declare, retry_policy,
                            signal=None, sender=None):
        try:
            if not DapperLocal.trace_switch():
                return
            log.debug("before_task_publish args is %s, %s" % (body, sender))

            span = CeleryTaskSpan()
            span.client_send(body, exchange, routing_key, headers, sender)
            body['span'] = span
        except:
            log.error("before task push dapper error: %s" % current_exception())

    @classmethod
    def after_task_publish(cls, body, exchange, routing_key, signal=None, sender=None):
        try:
            if not DapperLocal.trace_switch():
                return
            log.debug('after_task_publish for task id %s, %s, %s' % (body, sender, body['span']))
            span = body.pop('span', None)
            if span:
                span.client_receive(body, exchange, routing_key, sender)
        except:
            log.error("after task publish dapper error: %s" % current_exception())

    @classmethod
    def task_begin(cls, task_id, task, args, kwargs, signal=None, sender=None):
        try:
            if not DapperLocal.trace_switch() or not cls.dapper_local:
                return
            log.debug("task_begin args %s, kwargs %s " % (args, kwargs))

            context = LocalTrace.headers_to_bean(DapperLocal.service_name, task.request.headers)
            DapperLocal.start(context, task.name)

            span = CeleryTaskSpan()
            span.server_receive(task_id, task, args, kwargs, sender)
            setattr(task, 'celery_span', span)
        except:
            log.error("task begin dapper error: %s" % current_exception())

    @classmethod
    def task_end(cls, task_id, task, args, kwargs, retval, state, signal=None, sender=None):
        try:
            if not DapperLocal.trace_switch() or not cls.dapper_local:
                return
            log.debug("task_end args %s, kwargs %s, state is %s " % (args, kwargs, state))

            span = getattr(task, 'celery_span', None)
            if span:
                span.server_send(task_id, task, args, kwargs, retval, state, sender)
            delattr(task, 'celery_span')

            DapperLocal.end()
        except:
            log.error("task end dapper error: %s" % current_exception())

    @classmethod
    def task_fail(cls, task_id, exception, args, kwargs, traceback, einfo, signal=None, sender=None):
        if not DapperLocal.trace_switch():
            return
        log.error("task_fail %s " % task_id)

    @classmethod
    def task_revoked(cls, request, terminated, signum, expired, signal=None, sender=None):
        if not DapperLocal.trace_switch():
            return
        log.info("task_revoked request is %s" % request)

    def _client_send(self, body, exchange, routing_key, headers, sender):
        headers.update({Constants.DAPPER_HEADERS: LocalTrace.to_dapper_headers()})

        self.set_span("celery publish")
        self.set_endpoint(ipv4=local_ip_int, port=6379)

        self.add_annotation(Constants.CLIENT_SEND)
        self.add_binary(TraceKeys.CELERY_TASK_ID, body['id'])
        self.add_binary(TraceKeys.CELERY_TASK_NAME, sender)
        self.add_binary(TraceKeys.CELERY_TASK_PARAMETER, to_json_no_tab((body['args'], body['kwargs'])))
        self.add_binary(TraceKeys.CELERY_EXCHANGE, exchange)
        self.add_binary(TraceKeys.CELERY_ROUTING_KEY, routing_key)

    def _client_receive(self, body, exchange, routing_key, sender):
        self.add_annotation(Constants.CLIENT_RECV)

    def _server_receive(self, task_id, task, args, kwargs, sender):
        self.set_span("celery task execute")
        self.set_endpoint(ipv4=local_ip_int, port=6379)
        self.add_annotation(Constants.SERVER_RECV)

    def _server_send(self, task_id, task, args, kwargs, retval, state, sender):
        self.add_annotation(Constants.SERVER_SEND)
        self.add_binary(TraceKeys.CELERY_TASK_ID, task_id)
        self.add_binary(TraceKeys.CELERY_TASK_NAME, sender)
        self.add_binary(TraceKeys.CELERY_TASK_PARAMETER, to_json_no_tab((args, kwargs)))
        self.add_binary(TraceKeys.CELERY_TASK_STATE, state)

    @classmethod
    def add_publish_signals(cls):
        from celery.signals import before_task_publish, after_task_publish
        before_task_publish.connect(cls.before_task_publish)
        after_task_publish.connect(cls.after_task_publish)

    @classmethod
    def add_run_signals(cls, dapper_local):
        from celery.signals import task_prerun, task_postrun, task_failure, task_revoked
        task_prerun.connect(cls.task_begin)
        task_postrun.connect(cls.task_end)
        task_failure.connect(cls.task_fail)
        task_revoked.connect(cls.task_revoked)

        cls.dapper_local = dapper_local


