import logging
mylogger = logging.getLogger("my")
mylogger.setLevel(logging.INFO)
file_handler = logging.FileHandler('my_spare.csv')
stream_hander = logging.StreamHandler()
mylogger.addHandler(file_handler)
mylogger.addHandler(stream_hander)
formatter = logging.Formatter('%(asctime)s,%(message)s')
stream_hander.setFormatter(formatter)
file_handler.setFormatter(formatter)

mylogger.info("start!!!")

import boto3
for i in range(10):
    import time
    time.sleep(5)

    from botocore.exceptions import ClientError
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName='HelloBOTO%d' %i,Description='Made by boto3',VpcId=vpc_id)
        security_group_id = response['GroupId']
        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        mylogger.info('Creation %s'%security_group_id)
    except ClientError as e:
        mylogger.info(e)
#여기부터 삭제 전처리
client = boto3.client('ec2')
list_GroupId =[]
result = client.describe_security_groups()
for value in result["SecurityGroups"]:
    list_GroupId.append(value["GroupId"])
# 여기부터 삭제
from botocore.exceptions import ClientError
ec2 = boto3.client('ec2')
for i in list_GroupId:
    try:
        response = ec2.delete_security_group(GroupId=i)
        mylogger.info('Deleted %s' %i)
        # print('Security Group Deleted')
    except ClientError as e:
        mylogger.info(e)
#s3 업로드
bucket_name='sanghyeon-python-bucket'
s3 = boto3.client('s3')
response = s3.list_buckets()
result= [bucket['Name'] for bucket in response['Buckets']]
if bucket_name in result:
    print('이미 있는 버킷이름입니다.')
else:
    print('만든다')
    s3 = boto3.client('s3', region_name="ap-southeast-1")
    response = s3.create_bucket(Bucket='sanghyeon-python-bucket',CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-1'})

s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucket_name)
bucket_object=[]
for awsfile in my_bucket.objects.all():
    bucket_object.append(awsfile.key)
if 'my.csv' in bucket_object:
    print('이미있어')
    f = open('my_spare.csv', 'r')
    content = f.read()
    f.close()
    import botocore
    KEY = 'my.csv'
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).download_file(KEY, 'my.csv')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    file = open("my.csv",'a')
    file.write(content)
    file.close()
    print('합쳤음')
    import os
    s3 = boto3.client('s3')
    files = os.listdir("./")

    s3.upload_file('my.csv', bucket_name, 'my.csv')
    print('업로드 완료')
else:
    import os
    s3 = boto3.client('s3')
    files = os.listdir("./")

    s3.upload_file('my.csv', bucket_name, 'my.csv')
    print('업로드 완료')
