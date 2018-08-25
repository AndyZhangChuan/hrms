# -*- encoding: utf8 -*-
import os
from core.configs.config_default import Config

HRMS_DB_USER_NAME = os.environ.get("HRMS_DB_USER_NAME")
HRMS_DB_IP = os.environ.get("HRMS_DB_IP")
HRMS_DB_PASSWORD = os.environ.get("HRMS_DB_PASSWORD")


class OnlineConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_BINDS = {
        'hrms': 'mysql://%s:%s@%s:3306/hrmsdb' % (HRMS_DB_USER_NAME, HRMS_DB_IP, HRMS_DB_PASSWORD)
    }

