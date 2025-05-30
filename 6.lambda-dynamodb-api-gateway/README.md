# Step-by-Step Guide: API Gateway + Lambda + DynamoDB Integration

This guide will walk you through building a serverless web application using Amazon API Gateway, AWS Lambda, and Amazon DynamoDB.

---

## ✅ Step 1: Create DynamoDB Table

1. Go to **AWS Console** → Search **DynamoDB** → Open the **Dashboard**
2. Click on **Create table**
3. Enter:

   * **Table name**: `veera`
   * **Partition key**: `email`
4. Click **Create**

> ⚠️ Note: If you use a different table name or partition key, update it in the Lambda function accordingly.

---

## ✅ Step 2: Create IAM Role for Lambda

1. Go to **IAM Console** → Click **Create role**
2. Select **Trusted entity**: `AWS service`
3. Use case: **Lambda**
4. Attach permission: `AdministratorAccess`
5. Click **Next** → Give the role a name → **Create role**

---

## ✅ Step 3: Create Lambda Function

1. Go to **Lambda Console** → Click **Create function**
2. Function name: `lambda-dynamodb-handler`
3. Runtime: `Python 3.x`
4. Click **Change default execution role** → Select **Use existing role**
5. Choose the IAM role created in Step 2
6. Click **Create function**

---

## ✅ Step 4: Add Lambda Function Code

1. Open the `lambda_function.py` file in the Lambda editor
2. Copy code from:
   [Lambda Function Code](https://github.com/CloudTechDevOps/project-api-lambda-dynamodb-intigration/blob/main/lambda_function.py)
3. Paste it into the editor and save

---

## ✅ Step 5: Create HTML Files (Optional Frontend)

### index.html (Input Form)

* Create a file `index.html`
* Paste code from:
  [index.html](https://github.com/CloudTechDevOps/project-api-lambda-dynamodb-intigration/blob/main/index.html)

### success.html (Success Page)

* Create a file `success.html`
* Paste code from:
  [success.html](https://github.com/CloudTechDevOps/project-api-lambda-dynamodb-intigration/blob/main/success.html)

---

## ✅ Step 6: Create API Gateway

1. Go to **API Gateway Console** → Click **Create API**
2. Select **REST API** → Click **Build**
3. Enter API name → Select **Regional** endpoint type
4. Click **Create API**

### Create GET Method:

* Click on the root resource `/`
* Click **Create method** → Choose **GET**
* Enable **Lambda Proxy Integration**
* Link to the Lambda function created earlier → Click **Create method**

### Create POST Method:

* Repeat the same steps but choose **POST** instead of **GET**

---

## ✅ Step 7: Deploy API

1. Click **Actions** → **Deploy API**
2. Select **New Stage** → Stage name: `dev`
3. Click **Deploy**
4. Copy the **Invoke URL** (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/dev`)

---

## ✅ Step 8: Test the Application

1. Paste the invoke URL in your browser
2. Submit data via `index.html` form
3. On success, `success.html` is shown
4. Open **DynamoDB** → Table `veera` → **Explore items**
5. You should see the record inserted

---

## ✅ Benefits of This Architecture

* **Serverless**: No server management needed
* **Scalable**: Handles traffic spikes automatically
* **Cost-effective**: Pay only for what you use
* **Decoupled**: Each service (API Gateway, Lambda, DynamoDB) has its own responsibility

---

🎉 **Congratulations!** You've successfully built and deployed a serverless web application using Lambda, DynamoDB, and API Gateway.
