#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/17'
"""


# Project Modules
from .. import retry_for_requests
from .ucloud_common import UCloudCommon


def get_config(c):
    return {
        'public_key': c.get('AccessKeyId'),
        'private_key': c.get('AccessKeySecret'),
    }


class UCloudClient(object):
    def __init__(self, config=None):
        self.config = config
        self.common_client = UCloudCommon(**get_config(config))

    def verify(self):
        return self.common_client.verify()

    @retry_for_requests
    def common(self, **biz_params):
        return self.common_client.call(**biz_params)
