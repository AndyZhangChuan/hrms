# -*- encoding: utf8 -*-

import os, sys

__author__ = 'zhangchuan'

def get_project_dir():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    pps = file_dir.split("/")
    return "/".join(pps[:-2])

def add_sys_path(path):
    sys.path.append(path)

project_dir = get_project_dir()

def load_all_path():
    add_sys_path(project_dir)
    add_sys_path("%s/%s" % (project_dir, 'common'))
    add_sys_path("%s/%s" % (project_dir, 'core'))

load_all_path()