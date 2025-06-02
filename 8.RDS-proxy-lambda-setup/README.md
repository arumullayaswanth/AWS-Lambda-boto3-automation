# Lambda RDS Proxy Integration with Secrets Manager - Step-by-Step Guide

**<table style="width: 100%; margin-bottom: 20px;">
  <tr>
    <td align="center" style="padding: 10px; background-color: #e9f7f5; border-radius: 8px;">
      <img src="https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/blob/d11bffd5516f46e160bac3bee4f17d931a9f7f72/8.RDS-proxy-lambda-setup/images.png" width="1000%" style="border: 2px solid #ddd; border-radius: 10px;">
      <br><b> Lambda RDS Proxy </b>
    </td>
  </tr>
</table>**
---

## ✅ Step 1: Set Up Your RDS Database

1. Go to **AWS Console** → Search `RDS` → Open **Dashboard** → Click **Create database**
2. Choose:

   * **Database creation method**: Standard create
   * **Engine options**: MySQL
   * **Templates**: Free tier
3. Configure:

   * **DB Instance Identifier**: `mydbinstance`
   * **Master Username**: `admin`
   * **Master Password**: `******`
   * **Public access**: No
4. Click **Create database**
5. Note credentials:

   * **Endpoint**: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
   * **Username**: `admin`
   * **Password**: `******`

---

## ✅ Step 2: Store DB Credentials in Secrets Manager

### Step 2.1: Open Secrets Manager

* Go to **AWS Console** → Search `Secrets Manager` → Click **Store a new secret**

### Step 2.2: Choose Secret Type

* **Secret type**: Credentials for Amazon RDS database
* **Username**: `admin`
* **Password**: `******`

### Step 2.3: Choose Database

* **Database**: Select `mydbinstance`

### Step 2.4: Configure Secret

* **Secret name**: `dbsecrets`

### Step 2.5: Enable Automatic Rotation

* **Time unit**: Weeks
* **Weeks**: 1
* **Day**: Monday
* **Rotate immediately**
* **Rotation function**: Create using `secretsmanager:mysql` template
* Click **Next → Store**

---

## ✅ Step 3: Create Amazon RDS Proxy

1. Go to **RDS** → Select `mydbinstance` → Click **Actions → Create RDS proxy**
2. Configure:

   * **Engine family**: MariaDB and MySQL
   * **Proxy identifier**: `my-rds-proxy`
   * **Database**: Select `mydbinstance`
   * **Secrets Manager secrets**: Select `dbsecrets`
   * Choose **VPC**, **subnets** (same as RDS), and **security groups** (allow inbound from Lambda)
3. Click **Create proxy**
4. Note your proxy endpoint:

   * `my-rds-proxy.proxy-c0n8k0a0swtz.us-east-1.rds.amazonaws.com`

---

## ✅ Step 4: Create IAM Role for Lambda

1. Open **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity: AWS service → Use case: Lambda
3. Attach policy: `AdministratorAccess`
4. Role name: `Lambda-admin`
5. Click **Create role**

---

## ✅ Step 5: Create Lambda Function

1. Go to **Lambda Console** → Click **Create Function**
2. Set:

   * **Function name**: `lambda-rdsconnect`
   * **Runtime**: Python 3.x
   * **Execution role**: `Lambda-admin`
3. Click **Create function**
4. Update general configuration if needed

---

## ✅ Step 6: Install pymysql and Create Lambda Layer

### Step 6.1: Create S3 Bucket

* Name: `lambda-packages-pymysql-s3`
* Uncheck **Block Public Access**
* Enable **Bucket Versioning**

### Step 6.2: Create IAM Role for EC2

* Role name: `ec2-admin`
* Policy: `AdministratorAccess`

### Step 6.3: Launch EC2 Instance

* AMI: Amazon Linux 2
* Type: t2.micro
* IAM Role: `ec2-admin`
* Allow all traffic

### Step 6.4: Connect to EC2 and Install pymysql

```bash
sudo -i
yum install python3-pip -y
mkdir -p my_layer/python
pip3 install pymysql -t my_layer/python
yum install tree -y
cd my_layer
zip -r ../pymysql_layer.zip python/
aws s3 cp pymysql_layer.zip s3://lambda-packages-pymysql-s3
```

### Step 6.5: Create Lambda Layer

* Name: `dblayer`
* Upload via: **Amazon S3 link URL**
* S3 URI: `s3://lambda-packages-pymysql-s3/pymysql_layer.zip`
* Compatible runtime: Python 3.9
* Copy Layer ARN: `arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1`

---

## ✅ Step 7: Configure Lambda

### Add Layer to Lambda

1. Go to your Lambda function → **Layers** → **Add a layer**
2. Choose: **Specify an ARN**
3. Paste: `arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1`
4. Click **Add**


### Lambda Function Code

```python
import json            # To parse JSON strings (for secrets)
import boto3           # AWS SDK for Python, used to interact with AWS services (Secrets Manager here)
import pymysql         # MySQL client library for Python

# Define the database and table names you want to create
new_db_name = "test"
table_name = "mytable"

# Function to retrieve the database credentials stored in AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client('secretsmanager')                  # Create a Secrets Manager client
    response = client.get_secret_value(SecretId=secret_name) # Retrieve the secret using the secret's name
    return json.loads(response['SecretString'])              # Parse the secret JSON string and return as dict

# Function to connect to the RDS instance using the retrieved secret credentials
def connect_to_rds(secret):
    connection = pymysql.connect(
        host=secret['host'],               # Hostname of the RDS instance (from secret)
        user=secret['username'],           # Username (from secret)
        password=secret['password'],       # Password (from secret)
        cursorclass=pymysql.cursors.DictCursor  # Return query results as dictionaries
    )
    return connection                    # Return the DB connection object

# Main Lambda function handler, triggered on Lambda invocation
def lambda_handler(event, context):
    secret_name = "dbsecrets"            # replace you Secrets Manager secret name containing DB credentials
    connection = None                   # Initialize connection variable

    try:
        # Retrieve DB credentials from AWS Secrets Manager
        secret = get_secret(secret_name)
        
        # Establish connection to the RDS database
        connection = connect_to_rds(secret)
        
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist already
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            
            # Switch to the newly created (or existing) database
            cursor.execute(f"USE {new_db_name};")

            # Define SQL query to create a table if it doesn't exist
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,          -- Auto-increment primary key column 'id'
                name VARCHAR(255) NOT NULL,                 -- 'name' column, non-null string up to 255 chars
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp column defaults to current time
            );
            """
            # Execute the table creation query
            cursor.execute(create_table_sql)

        # Return success response
        return {
            'statusCode': 200,
            'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
        }

    except Exception as e:
        # Print and return the error message if anything fails
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        # Close the database connection if it was opened
        if connection:
            connection.close()

```

---

## ✅ Step 8: Create VPC Interface Endpoint for Secrets Manager

### Step 8.1: Open VPC Dashboard

* Go to **Endpoints** → **Create Endpoint**

### Step 8.2: Configure Endpoint

* Name: `AWS-endpoint`
* Service Name: `com.amazonaws.us-east-1.secretsmanager`
* VPC: Select your VPC

### Step 8.3: Select Subnets and Security Group

* Subnets: One private subnet per AZ
* Security Group: Allow outbound HTTPS (port 443)

### Step 8.4: Enable DNS and Policy

* Enable DNS
* Policy: Full access

### Step 8.5: Verify

* Ensure **State** is `Available`
Test Lambda's ability to retrieve secrets after the VPC endpoint is active.
---

## ✅ Step 9: Attach Lambda Function to VPC

* Go to Lambda → Click your function name: lambda-rdsconnect → Configuration → VPC → Edit
* Choose:

  * VPC: same as endpoint
  * Subnets: private
  * Security Group: allows port 443

---

## ✅ Step 10: Deploy and Test Lambda

* Deploy and create a test event
* Expected result:

```json
{
  "statusCode": 200,
  "body": "Database 'test' and table 'mytable' created successfully."
}
```

---

## ✅ Step 11: Connect from  EC2

### Allow 3306 in RDS Security Group



### Connect from EC2

```bash
ssh -i "your-key.pem" ec2-user@<EC2 Public IP>
sudo yum install mysql -y
mysql -h my-rds-proxy.proxy-c0n8k0a0swtz.us-east-1.rds.amazonaws.com -u admin -p
```

### SQL Commands

```sql
SHOW DATABASES;
USE test;
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO employees (name, role) VALUES
('Alice', 'Engineer'),
('Bob', 'Manager'),
('Carol', 'Analyst');
SELECT * FROM employees;
```

### Expected Output

```
+----+--------+---------+---------------------+
| id | name   | role    | created_at          |
+----+--------+---------+---------------------+
|  1 | Alice  | Engineer| 2025-06-02 10:00:00  |
|  2 | Bob    | Manager | 2025-06-02 10:01:00  |
|  3 | Carol  | Analyst | 2025-06-02 10:02:00  |
+----+--------+---------+---------------------+
```

---

**End of Guide**
