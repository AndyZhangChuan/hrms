# -*- coding: utf-8 -*-
import json

class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """

    def __init__(self, message='', code=0, *args, **kwargs):
        self.message = message
        self.code = code

    def getMessage(self):
        return {'message': self.message}

    def getErrorCode(self):
        return self.code

    def __str__(self):
        return json.dumps({'msg': self.message.encode('utf-8'), 'error_code': self.code})


class NetWorkError(ValueError):
    """
    Raised when net connection error
    """

    def __init__(self, message=''):
        self.message = message

    def getMessage(self):
        return {'message': self.message}
