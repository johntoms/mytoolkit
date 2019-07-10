#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/17'
"""

# Build-in Modules
import hashlib
from urllib.parse import urlencode
from urllib.request import urlopen
import json


class UCloudCommon(object):
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    @staticmethod
    def _verify_ac(private_key, params):
        items = params.items()
        items = sorted(items, key=lambda x:x[0])

        params_data = ""
        for key, value in items:
            params_data = params_data + str(key) + str(value)

        params_data = params_data + private_key

        '''use sha1 to encode keys'''
        hash_new = hashlib.sha1()
        hash_new.update(bytes(params_data, 'utf-8'))
        hash_value = hash_new.hexdigest()
        return hash_value

    @staticmethod
    def percent_encode(string):
        string = string.replace('+', '%20')
        string = string.replace('*', '%2A')
        string = string.replace('%7E', '~')
        string = string.replace('"', '%22')
        return string

    def verify(self):
        api_res = self.call(Action='GetRegion')
        if api_res.get('RetCode') > 0:
            return False

        return True

    def call(self, **params):
        params.update(PublicKey=self.public_key)
        signature = self._verify_ac(private_key=self.private_key, params=params)
        params.update(Signature=signature)
        url = 'https://api.ucloud.cn?' + self.percent_encode(
            urlencode(sorted(params.items(), key=lambda x: x[0])))
        response = urlopen(url=url)
        return json.loads(response.read())
