#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/16'
"""

from Chaos import Chaos
import time
import datetime
import os
# AK = {
#     "AccessKeyId": os.environ.get("AccessKeyId", "example"),
#     "AccessKeySecret": os.environ.get("AccessKeySecret", "example")
# }


# client  = AliyunClient(AK)
#
# response = client.common("ecs", Action="DescribeRegions")
# print(client.oss('GET', **{"max-keys": 1000}))
# print(client.oss('GET', BucketName='cxp-test', Query={'acl': None}))
# print(response)


# print(Chaos.AliyunClient(AK).common('ecs', Action='DescribeRegions'))
# print(Chaos.UCloudClient(AK).common(Action='DescribeEIP', Region='cn-bj2', ProjectId='org-u3lqre'))

# print(Chaos.TencentClient(AK).common("cvm", Action="DescribeRegions"))
# print(Chaos.AWSClient(AK).boto3('ec2', 'cn-north-1').describe_instances())


# 1. 创建 client
AK = {
    "AccessKeyId":"",
    "AccessKeySecret": "",
}
# ucloud_client = Chaos.TencentClient(AK)
#
# print(ucloud_client.common('cvm', Action='DescribeRegions'))
# print(ucloud_client.common('cvm', Action='DescribeInstances', Region='ap-shanghai'))
# # 2. 直接调用
# print(Chaos.TencentClient(AK).common("cvm", Action="DescribeRegions"))
#

# print(Chaos.AliyunClient(AK).common('ecs', Action='DescribeRegions'))

## 华东二金融云
start_time = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y-%m-%dT%H:%M:%SZ')
end_time = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
## cn-shanghai-finance-1
print(Chaos.AliyunClient(AK).common('rds', Action='DescribeDBInstances', RegionId='cn-shanghai'))
print(Chaos.AliyunClient(AK).common('rds', Action='DescribeSlowLogRecords', DBInstanceId='rm-uf679e820jx04jnvx',StartTime='2019-06-14T08:40Z', EndTime='2019-06-14T09:40Z'))
print(time.time())
