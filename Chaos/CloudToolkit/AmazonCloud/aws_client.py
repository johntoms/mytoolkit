#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/19'
"""

import boto3
# 3rd-part Modules
import botocore


def get_config(c):
    return {
        'aws_access_key_id': c.get('AccessKeyId'),
        'aws_secret_access_key': c.get('AccessKeySecret'),
    }


class AWSClient(object):
    def __init__(self, config=None):
        self.config = config
        self.client_map = {}

    def verify(self):
        try:
            self.boto3('ec2', 'cn-north-1').describe_regions()

        except botocore.exceptions.ClientError:
            return False

        else:
            return True

    def boto3(self, service, region):
        client_map_key = '{}/{}'.format(service, region)
        try:
            return self.client_map[client_map_key]

        except KeyError:
            boto3_config = get_config(self.config)
            boto3_config['service_name'] = service
            boto3_config['region_name'] = region
            self.client_map[client_map_key] = boto3.client(**boto3_config)

            return self.client_map[client_map_key]
