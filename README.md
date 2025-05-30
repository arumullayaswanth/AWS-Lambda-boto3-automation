


# AWS Lambda Function Use Cases

## ✅ Use Cases with Links

1. 🚀 **Push logs to CloudWatch to S3 automatically**  
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/2.Cloudwatch-to-s3-exporter)

2. 🔧 ** By using Lambda we have connected RDS via Private connection**  
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/3.lambda-rds-db-setup)

3. ⏰ **Lambda Event-based and Schedule-based Execution**  
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/2.Cloudwatch-to-s3-exporter)

4. 📦 **Lambda Layers for Custom Packages**  
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/blob/master/3.lambda-rds-db-setup/README.md)

5. 🌐 **CloudFront + Lambda Automation for Edge Location Updates**
   
   Note: CloudFront Lambda automation updates data inside edge locations when the developer pushes the updated changes (invalidations/updates)
   
   [🔗 GitHub Link](https://github.com/arumullayaswanth/aws-s3-cloudfront-lambda-automation-project)

6. 🔌 **Integrate API Gateway, Lambda, and RDS (tested via Postman)**
   
   Note: Integrate API Gateway and Lambda function and RDS, tested from the backend code deployed into Lambda function and tested to RDS by API methods using Postman tool
   
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/5.lambda-rds-api-gateway)

7. 💻 **Same process done with Backend EC2 combinations**  
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/4.Python-backend-testing)

8. 🗄️ **Deploy App in Lambda, use API Gateway, and DynamoDB**
    
    Note: Deploy an application in AWS Lambda function and configure to DynamoDB and try to access the API Gateway endpoint (frontend → backend → DynamoDB)
   
   [🔗 GitHub Link](https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/tree/master/6.lambda-dynamodb-api-gateway)





# AWS-Lambda-boto3-automation
Automate AWS cloud operations using AWS Lambda functions powered by Boto3. This repository contains Python scripts for event-driven automation of AWS services like EC2, S3, IAM, and more, enabling scalable and efficient cloud management.

# Installing boto3 in PyCharm (Step-by-Step Guide)

This guide will help you install the `boto3` library in your PyCharm project.

## Step 1: Open PyCharm

Launch PyCharm and open your project or create a new one.

## Step 2: Open the Python Interpreter Settings

1. Go to the top menu and click on `File`.
2. Select `Settings` (or `Preferences` on macOS).
3. In the left pane, navigate to `Project: <your_project_name>` > `Python Interpreter`.

## Step 3: Install boto3


1. Click on the **`+`** icon (Add Package) on the right side of the Python Interpreter window.
2. In the search bar, type `boto3`.
3. Select `boto3` from the list.
4. Click on the `Install Package` button at the bottom.
  
PyCharm will install the `boto3` library and its dependencies.
Make sure Python 3.x is installed on your machine.

Check the version by running:

```bash
python3 --version
```

or

```bash
python --version
```

[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) is the AWS SDK for Python. Install it using `pip`:

```bash
pip install boto3
```

## Step 4:  Configure AWS CLI Credentials

boto3 uses AWS credentials from your environment. You can configure them using AWS CLI.

### Install AWS CLI

If you don’t have AWS CLI installed, follow the instructions here:  
[Install AWS CLI - Official Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Configure Credentials

Run:

```bash
aws configure
```

You will be prompted for:

- **AWS Access Key ID**
- **AWS Secret Access Key**
- **Default region name** (e.g., `us-east-1`)
- **Default output format** (e.g., `json`)

## Step 4. Run the Script

Save your EC2 creation script (e.g., `create_ec2.py`) and run it:

```bash
python create_ec2.py
```

## Optional: Run Inside AWS Lambda

If you want to deploy this script as a Lambda function:

- You don’t need to install anything locally.
- Just package your code and upload it to Lambda.
- Ensure your Lambda execution role has the necessary permissions (e.g., EC2 full access or specific EC2 actions).

---

