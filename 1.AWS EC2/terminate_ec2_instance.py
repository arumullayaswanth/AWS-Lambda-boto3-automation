import boto3

# Initialize EC2 client
client = boto3.client('ec2', region_name='us-east-1')

# Terminate the EC2 instance (replace with your actual instance ID)
response = client.terminate_instances(
    InstanceIds=['i-00beb914604b13357']
)

# Print termination response
print("Termination initiated for instance: i-078ee7d9e02af3541")
print("Current state:", response['TerminatingInstances'][0]['CurrentState']['Name'])
