#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/19'
"""

from .tencentcloud_common import TencentCloudCommon
# Project Modules
from .. import retry_for_requests


def get_config(c):
    return {
        'access_key_id': c.get('AccessKeyId'),
        'access_key_secret': c.get('AccessKeySecret'),
    }


class TencentClient(object):
    def __init__(self, config=None):
        self.config = config
        self.common_client = TencentCloudCommon(**get_config(config))

    def verify(self):
        return self.common_client.verify()

    @retry_for_requests
    def common(self, product, timeout=10, **biz_params):
        return self.common_client.__getattr__(product)(timeout=timeout, **biz_params)
