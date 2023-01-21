import boto3

endpoint_url = 'https://storage.yandexcloud.net'
prefix = 'photo/'
bucket = 'booking'
s3_resource = boto3.resource("s3", endpoint_url=endpoint_url)
s3_bucket = s3_resource.Bucket(bucket)
service_chat = '-867115322'
