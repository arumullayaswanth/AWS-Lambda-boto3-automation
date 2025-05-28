# AWS Lambda to Connect to Amazon RDS (MySQL) - Step-by-Step Guide

**Author:** Yaswanth

---

## ✅ Step 1: Set Up Your RDS Database

1. Go to AWS Console → Search **RDS** → Dashboard → **Create database**
2. Choose a database creation method: **Standard create**
3. Engine options: **MySQL**
4. Templates: **Free tier**
5. Settings:

   * DB instance identifier: `mydbinstance`
   * Master username: `admin`
   * Master password: `*****`
   * Public access: `Yes`
6. Click **Create database**

### ✅ Note your RDS credentials:

* **Endpoint**: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* **Username**: `admin`
* **Password**: `******`

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

1. Go to **Lambda Console** → **Create Function**
2. Function name: `lambda-rdsconnect`
3. Runtime: **Python 3.x**
4. Execution role: `Lambda-admin`
5. Create the function
6. Update general configuration as needed and save

---

## ✅ Step 4: Install pymysql and Create Lambda Layer

### ✅ Step 4.1: Create S3 Bucket

1. Go to **Amazon S3** → **Create bucket**
2. Bucket type: General purpose
3. Bucket name: `lambda-packages-pymysql-s3`
4. Uncheck **Block Public Access**
5. Enable **Bucket Versioning**
6. Click **Create bucket**

### ✅ Step 4.2: Create IAM Role for EC2

1. Open **IAM Console** → **Roles** → **Create Role**
2. Trusted entity type: **AWS service**
3. Use case: **EC2**
4. Attach permission policy: `AdministratorAccess`
5. Role name: `ec2-admin`
6. Click **Create role**

### ✅ Step 4.3: Launch EC2 Instance

1. Go to **EC2 Console** → Click **Launch Instance**
2. Set Name: `ec2 server`
3. AMI: **Amazon Linux 2 AMI (HVM), Kernel 5.10**
4. Instance type: `t2.micro`
5. Key pair: `my-key-pair`
6. Network settings: Allow all traffic
7. IAM Role: `ec2-admin`
8. Storage: Default 8 GiB
9. Click **Launch Instance**

### ✅ Step 4.4: Connect to EC2 and Install pymysql

Run these commands:

```bash
sudo -i
yum install python3-pip -y
mkdir -p my_layer/python
pip3 install pymysql -t my_layer/python
yum install tree -y
cd my_layer
zip -r ../pymysql_layer.zip python/
cd
aws s3 cp pymysql_layer.zip s3://lambda-packages-pymysql-s3
```

Verify upload in S3 and copy the S3 URI:

```
s3://lambda-packages-pymysql-s3/pymysql_layer.zip
```

### ✅ Step 4.5: Create Lambda Layer

1. Go to **Lambda Console** → **Layers** → **Create layer**
2. Name: `dblayer`
3. Description: optional
4. Upload method: **Amazon S3 link URL**
5. S3 URI: `s3://lambda-packages-pymysql-s3/pymysql_layer.zip`
6. Compatible runtime: `Python 3.9`
7. Click **Create**

Copy the **Version ARN**:

```
arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1
```

---

## ✅ Step 5: Add Layer to Lambda

1. Go to your Lambda function → **Layers** → **Add a layer**
2. Choose: **Specify an ARN**
3. Paste: `arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1`
4. Click **Add**

---

## ✅ Step 6: Add Environment Variables

Set the following in Lambda → **Configuration → Environment variables**:

* `DB_HOST`: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* `DB_USER`: `admin`
* `DB_PASS`: `******`

---

## ✅ Step 7: Lambda Function Code

```python
import os
import pymysql
import boto3

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
new_db_name = "test"
table_name = "mytable"

def connect_to_rds():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def lambda_handler(event, context):
    connection = None
    try:
        connection = connect_to_rds()
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            cursor.execute(f"USE {new_db_name};")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            return {
                'statusCode': 200,
                'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
    finally:
        if connection:
            connection.close()
```

---

## ✅ Step 8: Deploy and Test

1. Click **Deploy** in Lambda Console
2. Click **Test**, create a test event
3. On success, you will see:

```json
{
  "statusCode": 200,
  "body": "Database 'test' and table 'mytable' created successfully."
}
```

---

## ✅ Step 9: Connect Your Database on External Workbench and EC2

### 🔹 A. Using MySQL Workbench

1. Open **MySQL Workbench** → Add new connection
2. Set:

   * Connection Name: `rds-test-db`
   * Hostname: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
   * Port: `3306`
   * Username: `admin`
   * Password: enter and store
3. Click **Test Connection**

✅ Ensure RDS security group allows TCP 3306 from your IP

### 🔹 B. Using EC2

1. SSH into EC2:

```bash
ssh -i "your-key.pem" ec2-user@<EC2 Public IP>
```

2. Install MySQL client:

```bash
sudo yum install mysql -y
```

3. Connect to RDS:

```bash
mysql -h mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com -u admin -p
```

4. Run SQL:

```sql
SHOW DATABASES;
```

Example Output:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
```

---

## 🎉 Success!

You now have:

* An RDS MySQL database
* A Lambda function that connects to it
* SQL logic that runs in a serverless environment
* Secure access from EC2 and external clients
