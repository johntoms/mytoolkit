#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/19'
"""

# -*- coding: utf-8 -*-

# Build-in Modules
import base64
import hashlib
import hmac
import random
import time
from urllib.request import quote

# 3rd-part Modules
import requests

# Project Modules
from .. import parse_response

PRODUCT_API_CONFIG_MAP = {
    'cvm': {
        'domain': 'cvm.tencentcloudapi.com',
        'version': '2017-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'bm': {
        'domain': 'bm.tencentcloudapi.com',
        'version': '2018-04-23',
        'port': 443,
        'protocol': 'https'
    },
    'cbs': {
        'domain': 'cbs.tencentcloudapi.com',
        'version': '2017-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'tke': {
        'domain': 'tke.tencentcloudapi.com',
        'version': '2018-05-25',
        'port': 443,
        'protocol': 'https'
    },
    'cis': {
        'domain': 'cis.tencentcloudapi.com',
        'version': '2018-04-08',
        'port': 443,
        'protocol': 'https'
    },
    'as': {
        'domain': 'as.tencentcloudapi.com',
        'version': '2018-04-19',
        'port': 443,
        'protocol': 'https'
    },
    'clb': {
        'domain': 'clb.tencentcloudapi.com',
        'version': '2018-03-17',
        'port': 443,
        'protocol': 'https'
    },
    'vpc': {
        'domain': 'vpc.tencentcloudapi.com',
        'version': '2017-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'cdb': {
        'domain': 'cdb.tencentcloudapi.com',
        'version': '2017-03-20',
        'port': 443,
        'protocol': 'https'
    },
    'redis': {
        'domain': 'redis.tencentcloudapi.com',
        'version': '2018-04-12',
        'port': 443,
        'protocol': 'https'
    },
    'mongodb': {
        'domain': 'mongodb.tencentcloudapi.com',
        'version': '2018-04-08',
        'port': 443,
        'protocol': 'https'
    },
    'mariadb': {
        'domain': 'mariadb.tencentcloudapi.com',
        'version': '2017-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'dcdb': {
        'domain': 'dcdb.tencentcloudapi.com',
        'version': '2018-04-11',
        'port': 443,
        'protocol': 'https'
    },
    'sqlserver': {
        'domain': 'sqlserver.tencentcloudapi.com',
        'version': '2018-03-28',
        'port': 443,
        'protocol': 'https'
    },
    'postgres': {
        'domain': 'postgres.tencentcloudapi.com',
        'version': '2017-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'cdn': {
        'domain': 'cdn.tencentcloudapi.com',
        'version': '2018-06-06',
        'port': 443,
        'protocol': 'https'
    },
    'yunjing': {
        'domain': 'yunjing.tencentcloudapi.com',
        'version': '2018-02-28',
        'port': 443,
        'protocol': 'https'
    },
    'cws': {
        'domain': 'cws.tencentcloudapi.com',
        'version': '2018-03-12',
        'port': 443,
        'protocol': 'https'
    },
    'ms': {
        'domain': 'ms.tencentcloudapi.com',
        'version': '2018-04-08',
        'port': 443,
        'protocol': 'https'
    },
    'monitor': {
        'domain': 'monitor.tencentcloudapi.com',
        'version': '2018-07-24',
        'port': 443,
        'protocol': 'https'
    },
}


def percent_encode(string):
    if string is None:
        raise Exception('AccessKeyId or AccessKeySecret is None')
    if not isinstance(string, (str, bytes, int)):
        raise TypeError('AccessKeyId or AccessKeySecret should be String')
    if isinstance(string, bytes):
        string.decode('utf-8')
    elif isinstance(string, int):
        string = str(string)
    else:
        string.encode('utf-8').decode('utf-8')

    string = quote(string, '')
    string = string.replace('+', '%20')
    string = string.replace('*', '%2A')
    string = string.replace('%7E', '~')

    return string


class TencentCloudCommon(object):
    '''
    QCloud common HTTP API
    '''

    def __init__(self, access_key_id=None, access_key_secret=None, *args, **kwargs):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def sign(self, domain, params_to_sign):
        canonicalized_query_string = ''

        sorted_params = sorted(params_to_sign.items(), key=lambda kv_pair: kv_pair[0])
        for k, v in sorted_params:
            canonicalized_query_string += str(k) + '=' + percent_encode(v) + '&'

        canonicalized_query_string = canonicalized_query_string[:-1]

        string_to_sign = 'POST' + domain + '/?' + canonicalized_query_string

        h = hmac.new(bytes(self.access_key_secret, 'utf-8'), bytes(string_to_sign, 'utf-8'), hashlib.sha1)
        signature = base64.encodebytes(h.digest()).strip()
        return signature.decode('utf-8')

    def verify(self):
        status_code, api_res = self.cvm(Action='DescribeRegions')
        if status_code >= 400 or (isinstance(api_res, dict) and api_res.get('Response', {}).get('Error')):
            return False

        return True

    def call(self, domain, version, port=80, protocol='http', timeout=3, **biz_params):
        api_params = {
            'Timestamp': int(time.time()),
            'Nonce': random.randint(1, 2 ** 32),
            'SecretId': self.access_key_id,
            'Version': version,
            'SignatureMethod': 'HmacSHA1',
        }

        api_params.update(biz_params)
        api_params['Signature'] = self.sign(domain, api_params)

        url = '{}://{}:{}/'.format(protocol, domain, port)

        resp = requests.post(url, data=api_params, timeout=timeout)
        parsed_resp = parse_response(resp)
        return resp.status_code, parsed_resp

    def __getattr__(self, product):
        api_config = PRODUCT_API_CONFIG_MAP.get(product)

        if not api_config:
            raise Exception('Unknow TencentCloud product API config. Please use `call()` with full API configs.')

        domain = api_config.get('domain')
        version = api_config.get('version')
        port = api_config.get('port')
        protocol = api_config.get('protocol')

        def f(timeout=3, **biz_params):
            return self.call(domain=domain, version=version, port=port, protocol=protocol, timeout=timeout,
                             **biz_params)

        return f
