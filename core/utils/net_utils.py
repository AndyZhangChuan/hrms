# -*- encoding: utf8 -*-
__author__ = 'zhangchuan'

import socket
import struct


def get_local_ip():
    myaddr = "127.0.0.1"
    try:
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
    except Exception, e:
        print e
    return myaddr


def get_eth_ip(eth_name):
    try:
        import fcntl
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', eth_name[:15]))[20:24])
    except:
        pass
    return get_local_ip()


local_ip = get_eth_ip('eth0')


def convert_ip_to_int(ip):
    ipv4 = struct.unpack('!i', socket.inet_aton(ip))[0]
    return ipv4


local_ip_int = convert_ip_to_int(local_ip)
