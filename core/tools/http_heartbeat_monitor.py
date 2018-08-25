__author__ = 'zhangchuan'

import pycurl
import time
from cStringIO import StringIO
from threading import Thread
from heatbeat_monitor import HeartbeatMonitor, HeartbeatLost, HeartbeatReceived, HeartbeatRunComplete
from core import log


class HttpHeartbeatMonitor(HeartbeatMonitor):

    def __init__(self, tick_interval=10):
        HeartbeatMonitor.__init__(self, tick_interval)
        self._started = False
        self._ping_thread = None
        self._multi_curl = None
        self._handles = []

    def start(self):
        if self._started:
            return

        self._multi_curl = pycurl.CurlMulti()
        self._handles = []
        for host, path in self.hosts.items():
            self._handles.append(self._init_req(host, path))

        self._started = True
        self._ping_thread = Thread(target=self.ping)
        self._ping_thread.setDaemon(True)
        self._ping_thread.start()

    def _init_req(self, host, path):
        req = pycurl.Curl()
        resp = StringIO()
        url = 'http://' + host + path
        req.setopt(pycurl.URL, url)
        req.setopt(pycurl.WRITEFUNCTION, resp.write)
        req.setopt(pycurl.TIMEOUT, self.tick_interval)
        req.response = resp
        req.host = host
        return req

    def stop(self):
        if not self._started:
            return
        self._started = False
        self._ping_thread.join()
        self._ping_thread = None
        self._multi_curl.close()

    def ping(self):
        log.info('heartbeat thread is up')
        run = 1
        while self._started:
            for req in self._handles:
                self._multi_curl.add_handle(req)
            then = time.time()
            # log.info('run %d' % run)

            # run requests should return within tick_interval
            self._run_requests()

            now = time.time()
            elapsed = now - then
            # log.info('run %d done in %f' % (run, elapsed))
            self._notify(HeartbeatRunComplete(run, now, elapsed))
            need_sleep = self.tick_interval - elapsed
            if need_sleep > 0:
                # log.info('sleep for %f' % need_sleep)
                time.sleep(need_sleep)
            run += 1
        log.info('heartbeat thread is down')

    def _run_requests(self):
        last_handle_count = len(self._handles)
        while True and self._started:
            handle_count = self._perform()
            self._multi_curl.select(self.tick_interval)
            if handle_count != last_handle_count:
                message_count, success_list, fail_list = self._multi_curl.info_read()
                for req in success_list:
                    used_time = req.getinfo(pycurl.TOTAL_TIME)
                    resp_code = req.getinfo(pycurl.RESPONSE_CODE)
                    if resp_code == 200:
                        self._notify(HeartbeatReceived(req.host, time.time(), used_time))
                    else:
                        self._notify(HeartbeatLost(req.host, time.time()))
                    self._multi_curl.remove_handle(req)
                for req, error_code, error_msg in fail_list:
                    self._notify(HeartbeatLost(req.host, time.time()))
                    self._multi_curl.remove_handle(req)
                last_handle_count = handle_count
            if handle_count == 0:
                break

    def _perform(self):
        handle_count = 0
        while True:
            ret, handle_count = self._multi_curl.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break
        return handle_count
