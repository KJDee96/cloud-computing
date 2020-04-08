import re
import boto3

instance_id = ["i-abcd1111"]
def lambda_handler(instance_id):
    instance_id = instance_id[0]
    ec2_client = boto3.client('ec2')

    private_subnets = []
    subnets = ec2_client.describe_subnets()["Subnets"]
    private_pattern = re.compile('^.*Private$')
    for subnet in subnets:
        for tag in subnet["Tags"]:
            if private_pattern.match(tag["Value"]):
                private_subnets.append(subnet["SubnetId"])

    elbv2_client = boto3.client('elbv2')
    target_group = elbv2_client.describe_target_groups()["TargetGroups"][0]["TargetGroupArn"]

    ec2instance = ec2_client.describe_instances(InstanceIds=[instance_id])
    for private_subnet in private_subnets:
        if ec2instance["Reservations"][0]["Instances"][0]["SubnetId"] == private_subnet:
            elbv2_client.register_targets(
                TargetGroupArn=target_group,
                Targets=[
                    {
                        'Id': ec2instance["Reservations"][0]["Instances"][0]["InstanceId"],
                    }
                ]
            )
