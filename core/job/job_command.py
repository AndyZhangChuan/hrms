# -*- encoding: utf8 -*-

from flask_script import Manager
import sys
from core.utils import current_exception

from core.log import getLogger
logger = getLogger(__name__)

JobCommand = Manager(usage='Perform job schedule')

loaded_modules = {}
add_paths = []


@JobCommand.option('-p', '--params', dest='job_params', default='', help='pass job params')
@JobCommand.option('-f', '--filename', dest='job_name', default='default', help="execute job")
def execute(job_name='default', job_params=''):
    if len(job_name) < 2:
        print ''' job's name length must large than 2'''
        sys.exit(0)

    job_class = get_job_class(job_name)
    from core.job.task import TaskRunnable
    if issubclass(job_class, TaskRunnable):
        job_instance = job_class()
    else:
        from core.job.task import TaskTemplateWrapper
        job_instance = TaskTemplateWrapper(job_class)
    job_instance.execute(extract_params(job_params))


def get_job_class(job_name):
    # test.TestJobClient.MyTask
    logger.debug("job_name is  %s" % job_name)
    # job_module_name = job_name

    # if "." in job_name:
    paths = str(job_name).split(".")
    from env_loader import project_dir
    path = project_dir
    for i in range(0, len(paths) - 2):
        path = path + "/" + paths[i]
        if path not in add_paths:
            try:
                sys.path.append(path)
                add_paths.append(path)
                logger.debug("add path %s", path)
            except:
                logger.error("add path error" % current_exception())

    job_module_name = paths[len(paths) - 2]
    job_class_name = paths[len(paths) - 1]

    logger.debug("module is %s, class is %s" % (job_module_name, job_class_name))

    if job_module_name not in loaded_modules:
        job_module = __import__(job_module_name)
        logger.debug("job_name[%s]'s job_module is %s" % (job_name, job_module))

        loaded_modules[job_module_name] = job_module
    else:
        job_module = loaded_modules[job_module_name]

    job_class = getattr(job_module, job_class_name)
    logger.debug("job_name[%s]'s job_class is %s" % (job_name, job_class))

    return job_class


def extract_params(job_params=None):
    logger.debug("original job_params is %s" % job_params)
    params_map = {}
    if not job_params and len(job_params) > 2:
        return params_map

    params = job_params.split("&")
    for p in params:
        if "=" in p:
            kv = p.split("=")
            params_map[kv[0]] = kv[1]

    return params_map
