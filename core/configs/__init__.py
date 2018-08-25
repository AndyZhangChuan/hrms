__author__ = 'zhangchuan'

import os

try:
    from core.configs.config_local import DevConfig as Config
except ImportError:
    from core.configs.config_default import Config

config = Config()

config.APP_ENV = os.getenv('APP_ENV', 'LOCAL')