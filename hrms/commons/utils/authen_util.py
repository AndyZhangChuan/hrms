# -*- encoding: utf8 -*-

import hashlib
import sys
from random import Random
from base64 import b64encode

reload(sys)
sys.setdefaultencoding('utf-8')


def get_rsa_sign_by_params(params, private_key, secret_key):
    private_key = crypto_util.PrivateKey(private_key)
    md5_sign = get_md5_by_params(params, secret_key)
    return b64encode(private_key.sign(md5_sign))


def get_md5_by_params(params, secret_key):
    m = hashlib.md5()
    sort_keys = sorted(params)
    result_list = ["{key}={value}".format(key=key, value=params[key]) for key in sort_keys]
    auth_str = "&".join(result_list) + secret_key
    m.update(auth_str)
    m_digest = m.hexdigest()
    return m_digest


def get_insurance_sign_by_params(params, secret_key):
    m = hashlib.md5()
    sort_keys = sorted(params)
    result_list = ["{key}={value}".format(key=key, value=params[key]) for key in sort_keys]
    auth_str = "&".join(result_list) + "&key=" + secret_key
    m.update(auth_str)
    m_digest = m.hexdigest()
    return m_digest


def get_md5_by_params_v2(params, secret_key):
    """
    对参数进行md5加密，该方法适用于mall-fusion项目API签名
    :return:
    """
    m = hashlib.md5()
    sort_keys = sorted(params)
    result_list = ["{key}{value}".format(key=key, value=params[key]) for key in sort_keys]
    auth_str = secret_key + "".join(result_list) + secret_key
    m.update(auth_str)
    m_digest = m.hexdigest()
    return m_digest


def md5(auth_str):
    m = hashlib.md5()
    m.update(auth_str)
    m_digest = m.hexdigest()
    return m_digest


def sign_api_with_sha1(params, secret_key):
    sorted_params = {}
    sorted_params.update(params)
    sorted_params.update({'secret': secret_key})
    sorted_keys = sorted(sorted_params)
    s = '&'.join(['%s=%s' % (key, sorted_params[key]) for key in sorted_keys])
    sign = hashlib.sha1(s).hexdigest()
    return sign


def del_last_str(origin_str):
    str_list = list(origin_str)
    str_list.pop()
    return "".join(str_list)


def generate_random_secret(random_length=32):
    result = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        result += chars[random.randint(0, length)]
    return result
