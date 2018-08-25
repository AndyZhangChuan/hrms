# -*- coding: utf-8 -*-

from functools import partial

from wtforms.validators import regexp
from wtforms.validators import InputRequired


__all__ = [
    'captcha',
    'email',
    'password',
    'hash_password',
    'phone_number',
    'telephone_number',
    'input_required'
]


PHONE_REGEXP = '^(13|15|18|14|17)\d{9}$'
TELEPHONE_REGEXP = '^(010\d{8})|(0[2-9]\d{9,10})$'
EMAIL_REGEXP = '^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*'
CAPTCHA_REGEXP = '^\d{4,6}$'
PASSWORD_REGEXP = '^\w{6,16}$'
HASH_PASSWORD_REGEXP = '^\w{32}$'

phone_number = partial(regexp, regex=PHONE_REGEXP, message=u'手机号码格式错误')

telephone_number = partial(regexp, regex=TELEPHONE_REGEXP, message=u'座机号码格式错误')

email = partial(regexp, regex=EMAIL_REGEXP, message=u'邮箱格式错误')

captcha = partial(regexp, regex=CAPTCHA_REGEXP, message=u'验证码错误')

password = partial(regexp, regex=PASSWORD_REGEXP, message=u'密码格式错误')

hash_password = partial(regexp, regex=HASH_PASSWORD_REGEXP, message=u'密码格式错误')


class DaInputRequired(InputRequired):
    """
    Validates that input was provided for this field.

    Note there is a distinction between this and DataRequired in that
    InputRequired looks that form-input data was provided, and DataRequired
    looks at the post-coercion data.
    """
    def __call__(self, form, field):
        if not field.raw_data:
            return super(DaInputRequired, self).__call__(form, field)
        if not field.raw_data[0]:
            data = field.raw_data[0]
            if not isinstance(data, int) and not isinstance(data, float):
                return super(DaInputRequired, self).__call__(form, field)

input_required = DaInputRequired
