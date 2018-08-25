# -*- encoding: utf8 -*-

import json
import re
import xmltodict
from core import app
from center.constants import constants
from driver.service.commons import web_bll
from driver.service.commons import weixin_module


MASK = '*'
MOBILE_PHONE_REGEX = re.compile(r'^[0-9]{11}$')


def xml_request2json(req):
    """
    把xml请求转换为json
    :param req:
    :return:
    """
    return xml2json(req.data)


def xml2json(xml_str):
    """
    把xml字符串对象转换为json
    :param xml_str:
    :return:
    """
    json_data = json.dumps(xmltodict.parse(xml_str))
    data = json.loads(json_data)
    return data


def phone_format(phone, split):
    """
    按固定格式加上分隔符格式化电话号码
    :param phone:
    :param split:
    :return:

    """
    phone_list = list(str(phone))
    result = ""
    for i in xrange(len(phone_list)):
        result += phone_list[i]
        if i in[2, 6]:
            result += split
    return result


def parse_site_link(link):
    if link == '':
        return '#'
    if link.__contains__('#!') and not link.__contains__("onepiece"):
        if not link.__contains__(constants.SHOP_INDEX_URI):
            link = app.config.get("HOST_URL") + constants.SHOP_INDEX_URI + link

        else:
            # 转换为微信授权链接
            if web_bll.get_source() == 'wx':
                return link

    href = insert_url_params(link, transporterId=web_bll.get_transporter_id(), userToken=web_bll.get_token(),
                             appName=web_bll.get_source())
    return href


def insert_url_params(url, **kwargs):
    """
    在url插入参数
    :param url:
    :param kwargs:
    :return:
    """
    if not url.__contains__("insert"):
        target_index = url.find("#!")
        if target_index < 0:
            target_index = url.find("#")
        if target_index < 0:
            target_index = url.find("?")
        symbol_index = url.find("?")
        symbol = "&" if url.__contains__("?") and symbol_index <= target_index else '?'
        redirect_url = "{0}insert=1".format(symbol)
    else:
        redirect_url = ''
    for key in kwargs:
        redirect_url += "&{0}={1}".format(key, kwargs[key])
    if url.__contains__("#!"):
        url = url.replace("#!", redirect_url+"#/!")
    elif url.__contains__("#/"):
        url = url.replace("#", redirect_url+"#")
    else:
        url = url + redirect_url
    return url


def get_pic_model(pic_url, width):
    new_pic_url = pic_url + "?imageView2/0/w/%s/" % width
    return new_pic_url


def bool2int(value):
    return 1 if value else 0


def add_mask(input_str):
    ret = input_str
    if input_str == None:
        ret = None
    elif re.match(MOBILE_PHONE_REGEX, input_str) != None:
        ret = input_str[:3] + MASK * 4 + input_str[-4:]
    elif len(input_str) > 2:
        ret = input_str[:1] + MASK * (len(input_str) - 2) + input_str[-1:]
    elif len(input_str) == 2:
        ret = input_str[0] + MASK
    return ret
