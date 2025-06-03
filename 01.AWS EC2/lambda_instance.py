import json
import boto3
# Initialize EC2 client
client = boto3.client('ec2', region_name='ap-south-1')

# Launch EC2 instance
response = client.run_instances(
    ImageId='ami-06031e2c49c278c8f',
    InstanceType='t2.micro',
    KeyName='mumbai-keypair',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'MyBoto3Instance'}]
        }
    ]
    
)

