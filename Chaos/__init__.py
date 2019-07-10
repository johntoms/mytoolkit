from Chaos.CloudToolkit.aliyun.aliyun_client import AliyunClient
from Chaos.CloudToolkit.ucloud.ucloud_client import UCloudClient
from Chaos.CloudToolkit.tencentcloud.tencentcloud_client import TencentClient
from Chaos.CloudToolkit.AmazonCloud.aws_client import AWSClient
from Chaos.mysql_datebase_export import Explore


class Chaos:
    AliyunClient = AliyunClient
    UCloudClient = UCloudClient
    TencentClient = TencentClient
    AWSClient = AWSClient
    Explore = Explore



