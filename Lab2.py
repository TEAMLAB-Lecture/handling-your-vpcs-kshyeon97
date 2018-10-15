
#web server instance 생성
import boto3

ec2 = boto3.resource('ec2', region_name="ap-southeast-1")
InstanceId_Tag = 0
instances = ec2.create_instances(
    NetworkInterfaces=[{'SubnetId': "subnet-e5898182", 'DeviceIndex': 0, 'Groups': ["sg-04261b52db85032f2"]}],
	ImageId='ami-008b4227b39308266',
	MinCount=1,
	MaxCount=1,
	KeyName="key_pair_for_lab",
	InstanceType="t2.micro"
    )
for instance in instances:
    InstanceId_Tag = instance.id
    print(instance.id, instance.instance_type)
ec2.create_tags(Resources=[InstanceId_Tag], Tags=[{'Key':'NAME', 'Value':'web server'}])
print("tag: web sever")

#crontab instance 생성
import boto3

ec2 = boto3.resource('ec2', region_name="ap-southeast-1")

instances = ec2.create_instances(
    NetworkInterfaces=[{'SubnetId': "subnet-e5898182", 'DeviceIndex': 0, 'Groups': ["sg-04261b52db85032f2"]}],
	ImageId='ami-0df4a80161d4c4b13',
	MinCount=1,
	MaxCount=1,
	KeyName="key_pair_for_lab",
	InstanceType="t2.micro"
    )

for instance in instances:
    InstanceId_Tag = instance.id
    print(instance.id, instance.instance_type)

ec2.create_tags(Resources=[InstanceId_Tag], Tags=[{'Key':'NAME', 'Value':'web server'}])
print("tag: crontab server")
