__author__ = 'zhangchuan'


class HeartbeatEvent:
    def __init__(self, address, time):
        self.address = address
        self.time = time


class HeartbeatLost(HeartbeatEvent):
    def __init__(self, address, time):
        HeartbeatEvent.__init__(self, address, time)


class HeartbeatReceived(HeartbeatEvent):
    def __init__(self, address, time, request_time):
        HeartbeatEvent.__init__(self, address, time)
        self.request_time = request_time


class HeartbeatRunComplete(HeartbeatEvent):
    def __init__(self, count, time, time_used):
        HeartbeatEvent.__init__(self, None, time)
        self.count = count
        self.time_used = time_used


class HeartbeatMonitor:
    def __init__(self, tick_interval):
        self.hosts = {}
        self.tick_interval = tick_interval
        self.listeners = []

    def start(self):
        pass

    def stop(self):
        pass

    def ping(self):
        pass

    def add_listener(self, listener):
        self.listeners.append(listener)

    def _notify(self, event):
        for listener in self.listeners:
            listener(event)
