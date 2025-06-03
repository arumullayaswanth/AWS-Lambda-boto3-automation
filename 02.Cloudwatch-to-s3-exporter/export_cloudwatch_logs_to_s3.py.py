import boto3
import gzip
import json
import time
from datetime import datetime

# Initialize AWS SDK clients
logs_client = boto3.client('logs')
s3_client = boto3.client('s3')

# S3 bucket name
S3_BUCKET_NAME = 'cloudwatchlogsec2'

# CloudWatch Log Group and Stream
LOG_GROUP = 'LOG-FROM-EC2'
LOG_STREAM = 'i-063e788f302fa4d8a'

def lambda_handler(event, context):
    # Get the current timestamp for file naming
    timestamp = time.time()
    file_name = f'logs-{int(timestamp)}.json.gz'

    # Get log events from CloudWatch Logs (last 24 hours)
    response = logs_client.get_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=LOG_STREAM,
        startTime=int(time.time() - 86400) * 1000,   # Get logs from the last 24 hours (in milliseconds) 
        endTime=int(time.time()) * 1000,            # now
        limit=10000     # Adjust based on the number of logs you want to fetch
    )

    # Collect log events
    log_events = []
    for event in response['events']:
        log_events.append(event)

    # Compress log data to gzip format
    log_data = json.dumps(log_events, default=str)
    compressed_log_data = gzip.compress(log_data.encode('utf-8'))

    # Upload compressed log file to S3
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=f'cloudwatch-logs/{file_name}',
        Body=compressed_log_data,
        ContentType='application/gzip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Logs exported successfully')
    }
