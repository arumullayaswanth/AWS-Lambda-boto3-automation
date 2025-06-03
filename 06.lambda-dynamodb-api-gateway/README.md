# Step-by-Step Guide: API Gateway + Lambda + DynamoDB Integration

This guide will walk you through building a serverless web application using Amazon API Gateway, AWS Lambda, and Amazon DynamoDB.




<table style="width: 100%; margin-bottom: 20px;">
  <tr>
    <td align="center" style="padding: 10px; background-color: #e9f7f5; border-radius: 8px;">
      <img src="https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/blob/32662ad798434062570eca8eb9c9408f2f0a108c/6.lambda-dynamodb-api-gateway/images.png" width="1000%" style="border: 2px solid #ddd; border-radius: 10px;">
      <br><b> Lambda-DynamoDB API Integration  architecture Project </b>
    </td>
  </tr>
</table>



---

## ✅ Step 1: Create DynamoDB Table

1. Go to **AWS Console** → Search **DynamoDB** → Open the Dashboard
2. Click on **Create table**
3. Enter the following:

   * **Table name**: `Yaswanth`
   * **Partition key**: `email`
4. Click **Create**

⚠️ Note: If you use a different table name or partition key, update it in the Lambda function accordingly.

---

## ✅ Step 2: Create IAM Role for Lambda

1. Open **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity type: **AWS service**
3. Use case: **Lambda**
4. Attach permission policy: `AdministratorAccess`
5. Role name: `Lambda-admin`
6. Click **Create role**

---

## ✅ Step 3: Create Lambda Function

1. Go to **Lambda Console** → Click **Create Function**
2. Function name: `lambda-DynamoDB`
3. Runtime: `Python 3.x`
4. Execution role: `Lambda-admin`
5. Click **Create function**
6. Update general configuration (e.g., timeout, memory) as needed and save

---

## ✅ Step 4: Lambda Function Code

Replace the default Lambda handler with the following code:

```python
import json
import os
import boto3

def lambda_handler(event, context):
    try:
        mypage = page_router(event['httpMethod'], event['queryStringParameters'], event['body'])
        return mypage
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def page_router(httpmethod, querystring, formbody):
    if httpmethod == 'GET':
        try:
            with open('index.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    elif httpmethod == 'POST':
        try:
            insert_record(formbody)
            with open('success.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

def insert_record(formbody):
    formbody = formbody.replace("=", "' : '")
    formbody = formbody.replace("&", "', '")
    formbody = "INSERT INTO yaswanth value {'" + formbody + "'}"   # Replace with DynamoDB Table name(My table name is Yashwant)

    client = boto3.client('dynamodb')
    response = client.execute_statement(Statement=formbody)
    # Assuming the execute_statement call returns successfully
    return response
```

---

## ✅ Step 5: Create Frontend Files

### Create `index.html` (Input Form)

1. Create a file named `index.html`
2. Paste your HTML form code inside

### Create `success.html` (Success Message)

1. Create a file named `success.html`
2. Paste your HTML thank-you message inside

---

## ✅ Step 6: Create API Gateway

1. Go to **API Gateway Console** → Click **Create API**
2. Choose **REST API** → Click **Build**
3. Set:

   * **API name**: `lambda-DynamoDB`
   * **Endpoint type**: `Regional`
4. Click **Create API**

### Create GET Method:

1. Click on the root resource `/`
2. Click **Create Method** → Select `GET`
3. Enable **Lambda Proxy Integration**
4. Link to your Lambda function: `lambda-DynamoDB`

### Create POST Method:

1. Click on the root resource `/`
2. Click **Create Method** → Select `POST`
3. Enable **Lambda Proxy Integration**
4. Link to your Lambda function: `lambda-DynamoDB`

---

## ✅ Step 7: Deploy API

1. Click **Actions** → **Deploy API**
2. Choose **New Stage**
3. Stage name: `dev`
4. Click **Deploy**
5. Copy the **Invoke URL**, e.g.:

   ```
   https://xyz.execute-api.us-east-1.amazonaws.com/dev
   ```



---

## ✅ Step 8: Test the Application

1. Open a browser and paste the invoke URL:


[https://xyz.execute-api.us-east-1.amazonaws.com/dev](https://xyz.execute-api.us-east-1.amazonaws.com/dev)


2. Submit the web form
3. Go to **DynamoDB** → Table `Yaswanth` → Click **Explore items**
4. You should see the submitted record

---

🎉 Congratulations! You have successfully built a full-stack serverless web form using AWS Lambda, API Gateway, and DynamoDB.


