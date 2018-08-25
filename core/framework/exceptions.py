# -*- coding: utf-8 -*-
"""
Global framework exception and warning classes.
"""


__all__ = [
    'ImproperlyConfigured',
]


class ImproperlyConfigured(Exception):
    """Framework is somehow improperly configured"""
    pass
