# -*- encoding: utf8 -*-
from core.configs.config_default import Config


class DevConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'mysql://root:a123456a@127.0.0.1:3306/hrms'
    SECRET_KEY = "test"
    SQLALCHEMY_BINDS = {
        'hrms': 'mysql://root:a123456a@127.0.0.1:3306/hrms',
        'hrms_slave': 'mysql://root:a123456a@127.0.0.1:3306/hrms'
    }

    REDIS_SERVER_HOST = "127.0.0.1"
    REDIS_SERVER_PORT = 6379
    REDIS_DATABASE_INDEX = 0
    REDIS_SOCKET_TIMEOUT = 0.1
