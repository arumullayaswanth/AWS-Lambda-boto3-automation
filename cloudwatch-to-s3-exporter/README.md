# CloudWatch Logs Collection and Export to S3 - Step-by-Step Guide

## ✅ Step 1: Create an IAM Role for EC2 Server

1. Open the **IAM Console**.
2. Click on **Roles** → **Create Role**.
3. Select **Trusted entity type**: AWS service.
4. Choose **Use case**: EC2.
5. Click **Next**.
6. Attach the following permission policy: `AdministratorAccess`.
7. Click **Next**.
8. Enter **Role name**: `ec2-admin`.
9. Click **Create role**.

---

## ✅ Step 2: Launch EC2 Instance

1. Go to the **EC2 Console** → Click **Launch Instance**.
2. Set **Name**: `ec2 server`.
3. Choose AMI: **Amazon Linux 2 AMI (HVM), Kernel 5.10**.
4. **Instance type**: `t2.micro`.
5. **Key pair**: `my-key-pair`.
6. **Network Settings**: Allow all traffic.
7. **IAM role**: `ec2-admin`.
8. **Storage**: Leave default (8 GiB).
9. Click **Launch Instance**.

---

## ✅ Step 3: Connect to EC2 Instance

Use your SSH client or EC2 Connect to log in to the instance.

---

## ✅ Step 4: Install the CloudWatch Agent

```bash
sudo yum install amazon-cloudwatch-agent -y
```

---

## ✅ Step 5: Create or Edit the Configuration File

```bash
sudo vi /opt/aws/amazon-cloudwatch-agent/bin/config.json
```

Paste the following JSON content:

```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/*",
            "log_group_name": "LOG-FROM-EC2",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 1
          }
        ]
      }
    }
  }
}
```

> ⚠️ Replace `LOG-FROM-EC2` with your custom log group name if needed.

---

## ✅ Step 6: Start the CloudWatch Agent

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
-a fetch-config \
-m ec2 \
-c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \
-s
```

---

## ✅ Step 7: 🔄 Optional - Verify Agent is Running

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
```

---

## ✅ Step 8: Verify CloudWatch Logs in AWS Console

1. Open the **CloudWatch Console**.
2. Navigate to **Logs** → **Log groups**.
3. Search for your log group (e.g., `LOG-FROM-EC2`).

---

## ✅ Step 9: Create S3 Bucket for Logs

1. Go to **Amazon S3** → **Create bucket**.
2. Choose bucket type: General purpose.
3. Name: `cloudwatchlogsec2`.
4. Click **Create bucket**.

### 🔐 Add Bucket Policy

Go to `cloudwatchlogsec2` → **Permissions** → **Bucket Policy** → **Edit bucket policy**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.us-east-1.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::cloudwatchlogsec2"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.us-east-1.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::cloudwatchlogsec2/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control",
                    "aws:SourceAccount": "421954350274"
                }
            }
        }
    ]
}
```

Click **Save changes**.

---

## ✅ Step 10: Export Logs from CloudWatch to S3

1. Go to **CloudWatch Console**.
2. Open `LOG-FROM-EC2` log group.
3. Click **Actions** → **View all exports to Amazon S3**.
4. Choose bucket: `cloudwatchlogsec2`.
5. Click **Export**.

---

## ✅ Step 10.1: Automate Export with Lambda

### Create Lambda Function

1. Go to **AWS Lambda** → **Create function**.
2. Choose: Basic information → Change default execution role.
3. Paste the code below:

```python
import boto3
import gzip
import json
import time
from datetime import datetime

logs_client = boto3.client('logs')
s3_client = boto3.client('s3')

S3_BUCKET_NAME = 'cloudwatchlogsec2'
LOG_GROUP = 'LOG-FROM-EC2'
LOG_STREAM = 'i-063e788f302fa4d8a'

def lambda_handler(event, context):
    timestamp = time.time()
    file_name = f'logs-{int(timestamp)}.json.gz'

    response = logs_client.get_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=LOG_STREAM,
        startTime=int(time.time() - 86400) * 1000,
        endTime=int(time.time()) * 1000,
        limit=10000
    )

    log_events = [event for event in response['events']]
    log_data = json.dumps(log_events, default=str)
    compressed_log_data = gzip.compress(log_data.encode('utf-8'))

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
```

4. Deploy the code and test.
5. Verify logs in the S3 bucket.

---

## ✅ Step 11: Schedule Lambda with EventBridge

1. Go to **Amazon EventBridge** → **Rules** → **Create rule**.
2. Set rule name: `lambda-s3`, rule type: `Schedule`.
3. Schedule pattern : >A fine-grained schedule that runs at a specific time, such as 8:00 a.m. PST on the first Monday of every month.
4. Schedule type : (Cron-based schedule)
5. Schedule pattern: `cron(0 18 * * ? *)`.
6. eg: Cron expression (cron(00),huurs(18),Day of month (\*),month(\*),Day of week(?),year(\*)).
7. Next
8. Select target(s) → target1 → Target types(AWS server) → Select a target(lambda funcation) 
9. Target: Lambda function `awsec2-logs`.
10. Complete rule creation.

---

## ✅ Step 11.1: Add Lambda Trigger

1. Add **Trigger** → **EventBridge (CloudWatch Events)**.
2. Choose existing rule: `lambda-s3`.
3. Click **Add**.

---

## ✅ Step 12: Amazon Simple Notification Service (SNS) Notification

1. Go to **Amazon SNS** → **Create topic**.
2. Type: Standard, Name: `cloudwatch-s3`.
3. Create subscription:

   * Protocol: Email
   * Enter your email and subscribe.
4. Confirm the subscription via your email.

---

## ✅ Step 12.1: Attach SNS to Lambda Failure

1. In Lambda, add destination:
2. Destination config:

   * Source: Asynchronous invocation
   * Condition: On failure
   * Destination type: SNS
   * Destination: `cloudwatch-s3`
3. Save configuration.

---

# 🎉 Project DONE!

