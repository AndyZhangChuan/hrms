__author__ = 'zhangchuan'

import os
from core.configs.config_online import OnlineConfig
from core.configs.config_local import DevConfig

if os.getenv('APP_ENV', 'LOCAL') == 'ONLINE':
    config = OnlineConfig()
else:
    config = DevConfig()

config.APP_ENV = os.getenv('APP_ENV', 'LOCAL')