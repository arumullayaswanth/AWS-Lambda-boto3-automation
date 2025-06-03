import boto3

# Initialize EC2 client
client = boto3.client('ec2', region_name='us-east-1')

# Launch EC2 instance
response = client.run_instances(
    ImageId='ami-0e58b56aa4d64231b',
    InstanceType='t2.micro',
    KeyName='my-Key pair',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'MyBoto3-Instance'}]
        }
    ]
)
