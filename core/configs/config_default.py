# -*- encoding:utf8 -*-

import os

root_path = os.path.dirname(os.path.abspath(__file__)) + '/../../'


class Config:
    def __init__(self):
        pass

    __APP_NAME__ = 'hrms'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    TEMPLATE_FOLDER = root_path + 'resource/templates'
    STATIC_FOLDER = root_path + 'resource/static'
    UPLOADED_IMAGES_DEST = root_path + 'resource/uploads'

    SQL_PRINT_RATIO = 0

    LOCAL_LOGGER_NAME = 'default'
    SQL_LOGGER_NAME = 'default'
    LOCAL_LOGGER_MEMORY_CAPACITY = 64
    SQL_LOGGER_MEMORY_CAPACITY = 64

    # log directory
    HRMS_DEBUG_LOG = "/tmp/hrms_debug.log"
    HRMS_ERROR_LOG = "/tmp/hrms_error.log"

