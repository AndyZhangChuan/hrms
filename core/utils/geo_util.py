# -*- encoding: utf8 -*-
__author__ = 'zhangchuan'

import math


def get_range_lat(lat, distance, distance_unit=1):
    """

    :param lat:
    :param distance:
    :param distance_unit:
    :return: 维度范围
    """
    adistance = float(distance) / distance_unit
    range_lat = (1.0 / 110) * adistance
    return lat - range_lat, lat + range_lat


def get_range_lng(lat, lng, distance, distance_unit=1):
    """

    :param lat: 纬度
    :param lng: 经度
    :param distance:
    :return:
    """
    adistance = float(distance) / distance_unit
    eve_lng = math.cos(lat * math.pi / 180) * 111.0
    distance_lng = (1.0 / eve_lng) * adistance
    return lng - distance_lng, lng + distance_lng


def rad(d):
    """

    :param d:
    :return:
    """
    return d * math.pi / 180.0


def distance_with_coordinator(lat1, lng1, lat2, lng2, distance_unit=1):
    """
    计算两点间距离
    :param lat1:
    :param lng1:
    :param lat2:
    :param lng2:
    :param distance_unit:
    :return:
    """
    rad_lat1 = rad(lat1)
    rad_lat2 = rad(lat2)
    a = rad_lat1 - rad_lat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(rad_lat1) *
                                math.cos(rad_lat2) *
                                math.pow(math.sin(b / 2), 2)
                                ))
    earth_radius = 6378.137
    s *= earth_radius * distance_unit
    return abs(s)
