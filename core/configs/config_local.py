# -*- encoding: utf8 -*-
from core.configs.config_default import Config


class DevConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/hrms'

    SQLALCHEMY_BINDS = {
        'hrms': 'mysql://root:123456@127.0.0.1:3306/hrms',
        'hrms_slave': 'mysql://root:123456@127.0.0.1:3306/hrms'
    }

