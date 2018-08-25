# -*- encoding: utf8 -*-

import sys
import traceback


def current_exception():
    """
    当前进程的异常信息
    """
    try:
        exc_type, exc_value, exc_tb = sys.exc_info()
        exc_list = traceback.format_exception(exc_type, exc_value, exc_tb)
        if len(exc_list) > 0:
            exc_list.insert(0, exc_list[len(exc_list) - 1])
            exc_list.pop(len(exc_list) - 1)
            return "".join(exc_list)
    except:
        pass
    return None


def xpath_get(mydict, path):
    """
    通过/a/b方式获取dict内的值

    """
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            try:
                x = int(x)
                elem = elem[x]
            except ValueError:
                elem = elem.get(x)
    except:
        pass

    return elem
