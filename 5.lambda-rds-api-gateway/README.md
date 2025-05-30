# Lambda-RDS API Integration - Step-by-Step Guide

This guide explains how to build a Python-based Lambda API using API Gateway to perform operations on an RDS MySQL database.


<table style="width: 100%; margin-bottom: 20px;">
  <tr>
    <td align="center" style="padding: 10px; background-color: #e9f7f5; border-radius: 8px;">
      <img src="https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation/blob/8125516f2363f5c565a0bbb0cb0d81110edaf2a3/5.lambda-rds-api-gateway/images.png" width="1000%" style="border: 2px solid #ddd; border-radius: 10px;">
      <br><b> Lambda-RDS API Integration  architecture Project </b>
    </td>
  </tr>
</table>

---

## ✅ Step 1: Set Up Your RDS Database

1. Go to AWS Console → Search **RDS** → Dashboard → Click **Create database**
2. Choose:

   * **Database creation method**: Standard create
   * **Engine options**: MySQL
   * **Templates**: Free tier
3. Settings:

   * **DB Instance Identifier**: `mydbinstance`
   * **Master Username**: `admin`
   * **Master Password**: `******`
   * **Public access**: Yes
4. Click **Create database**

### Note your RDS credentials:

* **Endpoint**: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* **Username**: `admin`
* **Password**: `******`

---

## ✅ Step 2: Connect to RDS in MySQL Workbench

1. Open **MySQL Workbench**

2. Connect using:

   * Hostname: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
   * Username: `admin`
   * Password: `******`

3. Run the following SQL commands:

```sql
CREATE DATABASE dev;
USE dev;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

SELECT * FROM dev.users;
```

---

## ✅ Step 3: Create IAM Role for Lambda

1. Open **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity: **AWS service**
3. Use case: **Lambda**
4. Attach permission: `AdministratorAccess`
5. Role name: `Lambda-admin`
6. Click **Create role**

---

## ✅ Step 4: Create Lambda Function

1. Go to **Lambda Console** → Click **Create Function**
2. Name: `lambda-rdsapi`
3. Runtime: Python 3.x
4. Execution role: `Lambda-admin`
5. Create function and save config

---

## ✅ Step 5: Lambda Function Code

Paste your Python code that handles GET and POST requests using `pymysql`. (See separate script `lambda_user_api.py`)

---

## ✅ Step 6: Add Environment Variables

Go to Lambda → Configuration → Environment variables and set:

* `DB_HOST`: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* `DB_USER`: `admin`
* `DB_PASSWORD`: `******`
* `DB_NAME`: `dev`

Click **Save**

---

## ✅ Step 7: Create Lambda Layer for pymysql

1. Download `pymysql_layer.zip` from GitHub or prepare locally
2. Go to **Lambda Console** → Layers → **Create layer**
3. Name: `dblayer`
4. Upload the zip file
5. Compatible runtime: Python 3.13
6. Click **Create**

### Copy the ARN:

```
arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1
```

---

## ✅ Step 8: Add Layer to Lambda Function

1. Go to your Lambda function → **Layers** → **Add a layer**
2. Choose: **Specify an ARN**
3. Paste the ARN:

```
arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1
```

4. Click **Add**

---

## ✅ Step 9: Create API Gateway

1. Go to AWS Console → Search **API Gateway**
2. Choose **REST API** → Click **Build**
3. Set API name: `test`
4. Click **Create API**

### Create GET Method:

* Integration type: Lambda Function
* Enable Lambda Proxy Integration
* Lambda Function: `lambda-rdsapi`

### Create POST Method:

* Integration type: Lambda Function
* Enable Lambda Proxy Integration
* Lambda Function: `lambda-rdsapi`

### Deploy API:

* Stage: New Stage
* Stage Name: `test`
* Click **Deploy**

### Copy the Invoke URL:

```
https://3askdhkde2.execute-api.us-east-1.amazonaws.com/test
```

---

## ✅ Step 10: Test with Postman

1. Go to [https://postman.com](https://postman.com)
2. Create new request:

   * Method: `POST`
   * URL: `https://3askdhkde2.execute-api.us-east-1.amazonaws.com/test`
   * Headers: `Content-Type: application/json`
   * Body (raw JSON):

```json
{
  "username": "yaswanth",
  "email": "yaswanth@example.com"
}
```

3. Click **Send**
4. Check your RDS table for new record
5. Create new request:

   * Method: GET
   * URL: `https://3askdhkde2.execute-api.us-east-1.amazonaws.com/test`
6. Click **Send**

---

🎉 You now have a fully working serverless API using Lambda, RDS, and API Gateway!
