__author__ = 'zhangchuan'

import time
import uuid
import json


class Timer:
    def __init__(self, logger, app_name='default'):
        self.started = False
        self.last_tick = 0
        self.start_time = 0
        self.request_id = 0
        self.logger = logger
        self.app_name = app_name

    def tick(self, prompt='', need_json=False):
        if not self.started:
            return
        now = time.time()
        elapsed = (now - self.last_tick) * 1000
        elapsed_total = (now - self.start_time) * 1000
        if need_json is True:
            self.logger(json.dumps({
                'app_name': self.app_name,
                'request_id': self.request_id,
                'phase': prompt,
                'elapsed': elapsed,
                'total': elapsed_total
            }))
        else:
            self.logger({
                'app_name': self.app_name,
                'request_id': self.request_id,
                'phase': prompt,
                'elapsed': elapsed,
                'total': elapsed_total
            })
        self.last_tick = now

    def start(self):
        self.started = True
        self.request_id = str(uuid.uuid1())
        self.start_time = time.time()
        self.last_tick = time.time()


def console_log(log):
    print '!------------->' + str(log)
