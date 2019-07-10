from Chaos.CloudToolkit.Aliyun.aliyun_client import AliyunClient
from Chaos.CloudToolkit.Acloud.ucloud_client import UCloudClient
from Chaos.CloudToolkit.TencentCloud.tencentcloud_client import TencentClient
from Chaos.CloudToolkit.AmazonCloud.aws_client import AWSClient
from Chaos.mysql_datebase_export import Explore


class Chaos:
    AliyunClient = AliyunClient
    UCloudClient = UCloudClient
    TencentClient = TencentClient
    AWSClient = AWSClient
    Explore = Explore



