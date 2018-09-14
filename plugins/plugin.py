# coding=utf-8
class Plugin:

    def __init__(self):

        pass


class Props:

    def __init__(self, type='', default=False, nullable=False, comment=''):
        """

        :param type: type只有string, number, bool, timestamp, list 和 object
        :param default:
        :param nullable:
        :return:
        """
        self.value = default
        self.type = type
        self.default = default
        self.nullable = nullable
        self.comment = comment

    def init(self, value):
        self.value = value if value else self.default


class Output:
    OK = 'ok'
    ERROR = 'error'
    RETURN = 'return'

    def __init__(self, status, content='', message=''):
        self.status = status
        self.content = content
        self.message = message

