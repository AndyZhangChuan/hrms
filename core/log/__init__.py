# -*- encoding: utf8 -*-
import sys
import logging
__author__ = 'zhangchuan'

DEFAULT_FORMAT = '%(asctime)s-%(name)s-%(levelname)s-%(process)d-%(processName)s-%(funcName)s %(message)s'


def getLogger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    default_handler = logging.StreamHandler(sys.stdout)
    default_handler.setLevel(logging.INFO)

    default_formatter = logging.Formatter(DEFAULT_FORMAT)
    default_handler.setFormatter(default_formatter)
    logger.addHandler(default_handler)

    return logger
