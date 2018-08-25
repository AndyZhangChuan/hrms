__author__ = 'zhangchuan'

import time


class Timer:
    def __init__(self, logger):
        self.started = False
        self.last_tick = 0
        self.start_time = 0
        self.logger = logger

    def tick(self, prompt=''):
        if not self.started:
            return
        now = time.time()
        elapsed = (now - self.last_tick) * 1000
        elapsed_total = (now - self.start_time) * 1000
        self.logger({prompt: '%.2f, %.2f' % (elapsed, elapsed_total)})
        self.last_tick = now

    def start(self):
        self.started = True
        self.start_time = time.time()
        self.last_tick = time.time()


def console_log(log):
    print '!------------->' + str(log)
