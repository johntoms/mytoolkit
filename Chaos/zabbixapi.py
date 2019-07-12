#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/7/12'
"""
# BuiltIn Packages
import os

# Part3   Packages
from pyzabbix import ZabbixAPI

# Project Packages


config  =  {
        'API_URL': os.environ.get('API_URL'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD')
}


class ZBX_API(object):
    def __init__(self, url, user, password):
        self.api = ZabbixAPI(url)
        self.user = user
        self.password = password
    def __enter__(self):
        self.api.login(user=self.user, password=self.password)
        return self.api

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.user.logout()
        print("exit")


# 实例化一个 api 对象
api = ZBX_API(user=config['USER'], url=config['API_URL'], password=config['PASSWORD'])

# 使用 with 进行操作，执行完后后会自动退出 zabbix，保证 zabbix 的 token 不会爆炸


with api as f:
    host_ids = f.host.get(output='hostids')
    print(host_ids)
