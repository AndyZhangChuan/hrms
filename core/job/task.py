# -*- encoding: utf8 -*-

import time
from datetime import datetime
from ..utils import current_exception
from ..utils.enum import enum
from ..utils.json_utils import trim_tab, to_json_no_tab

from ..log import getLogger
logger = getLogger(__name__)

__author__ = 'zhangchuan'


class TaskRunnable(object):

    def __init__(self):
        pass

    def execute(self, params=None):
        pass


class TaskTemplate(TaskRunnable):
    kafka_logger = None
    topic_task_log = "topic_task_execute_log_new"

    def __init__(self):
        super(TaskTemplate, self).__init__()
        self.result = None

    def get_task_name(self):
        return self.__class__.__name__

    def execute(self, params=None):
        if params is None:
            params = {}

        logger.debug("params is %s" % params)

        task_id = params.get('taskId', '1')

        logger.info("task[%s] execute start, task_id is %s" % (self, task_id))

        self.result = TaskResult.create(task_id)
        try:
            self.task_start()
            returned = self.run(params)
            execute_result = ""
            error_code = 0
            error_msg = None
            if isinstance(returned, TaskResult):
                if returned.is_success():
                    execute_result = returned.content
                else:
                    error_code = returned.error_code
                    error_msg = returned.error_msg
            else:
                execute_result = "Task[%s] execute result is %s" % (self.get_task_name(), to_json_no_tab(returned))

            self.task_end(execute_result, error_code=error_code, error_msg=error_msg)
        except:
            # print "task execute error: %s" % current_exception()
            logger.error("task run error: %s" % current_exception())
            self.task_end("", error_code=500, error_msg=current_exception())

        logger.info("task[%s] execute done, task_id is %s" % (self, task_id))

    def task_start(self):
        self.result.task_running()
        self.log_result()

    def task_end(self, content, error_code=0, error_msg=None):
        if error_code > 0 or error_msg is not None:
            self.result.task_fail(error_code, error_msg)
        else:
            self.result.task_success(content)
        self.log_result()

    def log_result(self):
        logger.info("no kafka logger: %s" % self.result.task_running())

    def get_logger(self):
        pass

    def run(self, params=None):
        """

        :return:
        """
        raise RuntimeError("implement this method in subclass")


class TaskTemplateWrapper(TaskTemplate):

    def __init__(self, job_class):
        super(TaskTemplateWrapper, self).__init__()
        self.job_class = job_class

    def run(self, params=None):
        self.job_class().run()


RUNNING = enum(value=1, name="RUNNING", text="运行中", css="label-info")
SUCCESS = enum(value=2, name="SUCCESS", text="成功", css="label-success")
FAIL = enum(value=3, name="FAIL", text="失败", css="label-danger")
UNKNOWN = enum(value=-1, name="UNKNOWN", text="未知", css="label-default")


class TaskResult(object):

    def __init__(self):
        self.task_id = ""
        self.status = UNKNOWN
        self.content = ""
        self.error_code = 0
        self.error_msg = ""
        self.start_time = 0
        self.end_time = 0
        self.project_id = 0
        self.job_id = 0

    @classmethod
    def create(cls, task_id):
        result = TaskResult()
        result.task_id = task_id
        return result

    def task_running(self):
        self.status = RUNNING
        self.start_time = int(time.time() * 1000)
        return self

    def task_success(self, content):
        self.status = SUCCESS
        self.content = content
        self.end_time = int(time.time() * 1000)
        return self

    def task_fail(self, error_code, error_msg):
        self.status = FAIL
        self.error_code = error_code
        self.error_msg = error_msg
        self.end_time = int(time.time() * 1000)
        return self

    def is_running(self):
        return RUNNING == self.status

    def is_success(self):
        return SUCCESS == self.status

    def is_fail(self):
        return FAIL == self.status

    def to_text(self):
        logging_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}".format(
            logging_time, self.task_id, self.status.name, trim_tab(self.content),
            self.error_code, trim_tab(self.error_msg), self.start_time, self.end_time,
            self.project_id, self.job_id
        )




