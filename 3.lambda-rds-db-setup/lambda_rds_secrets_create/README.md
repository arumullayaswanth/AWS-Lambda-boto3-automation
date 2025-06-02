## ✅ End-to-End AWS RDS & Lambda Configure AWS Secrets Manager for RDS Integration Guide

---

### ✅ Step 1: Set Up Your RDS Database

1. Go to **AWS Console → RDS → Dashboard → Create database**
2. Choose **Standard create**
3. **Engine options**: MySQL
4. **Templates**: Free tier
5. **Settings**:

   * DB instance identifier: `mydbinstance`
   * Master username: `admin`
   * Master password: `*****`
   * Public access: **No**
6. Click **Create database**

> ✅ **Note down**:
>
> * Endpoint: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
> * Username: `admin`
> * Password: `*****`

---

### ✅ Step 2: Create IAM Role for Lambda

1. Open **IAM Console → Roles → Create Role**
2. Trusted entity: **AWS service**, use case: **Lambda**
3. Attach policy: `AdministratorAccess`
4. Role name: `Lambda-admin`
5. Click **Create role**

---

### ✅ Step 3: Create Lambda Function

1. Go to **Lambda Console → Create Function**
2. Function name: `lambda-rdsconnect`
3. Runtime: `Python 3.x`
4. Execution role: **Use existing role** → `Lambda-admin`
5. Click **Create function**
6. Adjust general configuration as needed

---

### ✅ Step 4: Install pymysql and Create Lambda Layer

#### ✅ Step 4.1: Create S3 Bucket

1. Go to **Amazon S3 → Create bucket**
2. Name: `lambda-packages-pymysql-s3`
3. Uncheck **Block Public Access**
4. Enable **Versioning**
5. Click **Create bucket**

#### ✅ Step 4.2: Create IAM Role for EC2

1. Open **IAM Console → Roles → Create Role**
2. Trusted entity: **AWS service**, use case: **EC2**
3. Attach policy: `AdministratorAccess`
4. Role name: `ec2-admin`
5. Click **Create role**

#### ✅ Step 4.3: Launch EC2 Instance

1. Go to **EC2 Console → Launch Instance**
2. Name: `ec2-server`
3. AMI: `Amazon Linux 2 AMI`
4. Instance type: `t2.micro`
5. Key pair: `my-key-pair`
6. Network: Allow all traffic
7. IAM Role: `ec2-admin`
8. Storage: Default (8 GiB)
9. Click **Launch**

#### ✅ Step 4.4: Connect to EC2 and Install pymysql

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

> ✅ Copy S3 URI:
> `s3://lambda-packages-pymysql-s3/pymysql_layer.zip`

#### ✅ Step 4.5: Create Lambda Layer

1. Go to **Lambda Console → Layers → Create layer**
2. Name: `dblayer`
3. Upload via: **Amazon S3 link**
4. Paste: `s3://lambda-packages-pymysql-s3/pymysql_layer.zip`
5. Runtime: `Python 3.9`
6. Click **Create**
7. Copy Layer ARN:

> `arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1`

---

### ✅ Step 5: Add Layer to Lambda

1. Go to **lambda-rdsconnect → Layers → Add layer**
2. Choose: **Specify an ARN**
3. Paste the ARN above
4. Click **Add**

---

### ✅ Step 6: Configure AWS Secrets Manager for RDS

#### ✅ Step 6.1: Open Secrets Manager

1. Go to **Secrets Manager** → Click **Store a new secret**

#### ✅ Step 6.2: Choose Secret Type

* Type: **Credentials for Amazon RDS database**
* Enter:

  * Username: `admin`
  * Password: `*****`

#### ✅ Step 6.3: Choose Database

* Select: `mydbinstance`
* Click **Next**

#### ✅ Step 6.4: Configure Secret

* Secret name: `db-secret`
* Click **Next**

#### ✅ Step 6.5: Automatic Rotation

1. Enable rotation
2. Schedule: Every Monday
3. Select: **Create a rotation function**

   * Use template: `secretsmanager: mysql`
4. Click **Next → Store**

---

### ✅ Step 7: Lambda Function Code

```python
import json
import boto3
import pymysql

new_db_name = "test"
table_name = "mytable"

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

def connect_to_rds(secret):
    connection = pymysql.connect(
        host=secret['host'],
        user=secret['username'],
        password=secret['password'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def lambda_handler(event, context):
    secret_name = "db-secret"
    connection = None
    try:
        secret = get_secret(secret_name)
        connection = connect_to_rds(secret)
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            cursor.execute(f"USE {new_db_name};")
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_sql)
        return {
            'statusCode': 200,
            'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
    finally:
        if connection:
            connection.close()
```

---

### ✅ Step 8: Deploy and Test

* Click **Deploy**
* Create and run a test event
* On success, check logs and response body

---

### ✅ Step 9: Connect Your Database

#### 🔹 A. Using MySQL Workbench

* Connection Name: `rds-test-db`
* Hostname: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* Port: `3306`
* Username: `admin`
* Password: `*****`
* Click **Test Connection**
* ✅ Ensure RDS SG allows TCP 3306 from your IP

#### 🔹 B. Using EC2

```bash
ssh -i "your-key.pem" ec2-user@<EC2 Public IP>
sudo yum install mysql -y
mysql -h mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com -u admin -p
SHOW DATABASES;
```

> Expected Output:
> test, mysql, performance\_schema, etc.

---

✅ **You're done!** You’ve now set up an RDS MySQL instance, connected it securely via Lambda using AWS Secrets Manager and Lambda Layers, and validated the connection using both Lambda and EC2.

