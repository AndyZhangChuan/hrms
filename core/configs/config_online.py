# -*- encoding: utf8 -*-
import os
from core.configs.config_default import Config

HRMS_DB_USER_NAME = os.environ.get("HRMS_DB_USER_NAME")
HRMS_DB_IP = os.environ.get("HRMS_DB_IP")
HRMS_DB_PASSWORD = os.environ.get("HRMS_DB_PASSWORD")


class OnlineConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:3306/hrms_dev' % (HRMS_DB_USER_NAME, HRMS_DB_PASSWORD, HRMS_DB_IP)

    SQLALCHEMY_BINDS = {
        'hrms': 'mysql://%s:%s@%s:3306/hrms_dev' % (HRMS_DB_USER_NAME, HRMS_DB_PASSWORD, HRMS_DB_IP)
    }

