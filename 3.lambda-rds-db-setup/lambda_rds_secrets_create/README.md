## ✅ End-to-End AWS RDS & Lambda Configure AWS Secrets Manager for RDS Integration Guide


---

### ✅ Step 1: Set Up Your RDS Database

1. Go to **AWS Console** → Search **RDS** → Dashboard → **Create database**
2. Choose a database creation method: **Standard create**
3. Engine options: **MySQL**
4. Templates: **Free tier**
5. Settings:

   * DB instance identifier: `mydbinstance`
   * Master username: `admin`
   * Master password: `*****`
6. Connectivity:

   * Public access: **No**
7. Click **Create database**

✅ **Note your RDS credentials:**

* Endpoint: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* Username: `admin`
* Password: `******`

---

### ✅ Step 2: Create IAM Role for Lambda

1. Open **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity type: **AWS service**
3. Use case: **Lambda**
4. Attach permission policy: **AdministratorAccess**
5. Role name: `Lambda-admin`
6. Click **Create role**

---

### ✅ Step 3: Create Lambda Function

1. Go to **Lambda Console** → Click **Create Function**
2. Function name: `lambda-rdsconnect`
3. Runtime: **Python 3.x**
4. Execution role: Choose existing → **Lambda-admin**
5. Create the function
6. Update general configuration as needed and click **Save**

---

### ✅ Step 4: Install pymysql and Create Lambda Layer

#### ✅ Step 4.1: Create S3 Bucket

1. Go to **Amazon S3** → Click **Create bucket**
2. Bucket type: General purpose
3. Bucket name: `lambda-packages-pymysql-s3`
4. Uncheck **Block Public Access**
5. Enable **Bucket Versioning**
6. Click **Create bucket**

#### ✅ Step 4.2: Create IAM Role for EC2

1. Go to **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity type: **AWS service**
3. Use case: **EC2**
4. Attach policy: **AdministratorAccess**
5. Role name: `ec2-admin`
6. Click **Create role**

#### ✅ Step 4.3: Launch EC2 Instance

1. Go to **EC2 Console** → Click **Launch Instance**
2. Name: `ec2-server`
3. AMI: **Amazon Linux 2 AMI (HVM), Kernel 5.10**
4. Instance type: `t2.micro`
5. Key pair: `my-key-pair`
6. Network settings: Allow all traffic
7. IAM Role: `ec2-admin`
8. Storage: Default 8 GiB
9. Click **Launch Instance**

#### ✅ Step 4.4: Connect to EC2 and Install pymysql

Run the following:

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

Verify the upload in S3. Copy the S3 URI:

```
s3://lambda-packages-pymysql-s3/pymysql_layer.zip
```

#### ✅ Step 4.5: Create Lambda Layer

1. Go to **Lambda Console** → Layers → **Create layer**
2. Name: `dblayer`
3. Upload method: **Amazon S3 link URL**
4. S3 URI: `s3://lambda-packages-pymysql-s3/pymysql_layer.zip`
5. Compatible runtime: **Python 3.9**
6. Click **Create**
7. Copy the **Version ARN**:

```
arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1
```

---

### ✅ Step 5: Add Layer to Lambda

1. Go to **Lambda Console** → Your function → **Layers** → **Add a layer**
2. Choose: **Specify an ARN**
3. Paste:

```
arn:aws:lambda:us-east-1:421954350274:layer:dblayer-1:1
```

4. Click **Add**

---

### ✅ Step 6: Configure AWS Secrets Manager

#### ✅ Step 6.1: Open Secrets Manager

* Go to AWS Console → Search **Secrets Manager** → Click **Store a new secret**

#### ✅ Step 6.2: Choose Secret Type

* Secret type: **Credentials for Amazon RDS database**
* Username: `admin`
* Password: `******`

#### ✅ Step 6.3: Choose Database

* Select your RDS database: `mydbinstance`
* Click **Next**

#### ✅ Step 6.4: Configure Secret

* Secret name: `db-secret`
* Click **Next**

#### ✅ Step 6.5: Configure Automatic Rotation

1. Enable Automatic rotation
2. Schedule:

   * Time unit: **Weeks**
   * Weeks: `1`
   * Day: **Monday**
   * Select: **Rotate immediately**
3. Rotation function: **Create a rotation function**

   * Template: `secretsmanager:mysql`
4. Click **Next** → **Store**

---

### ✅ Step 7: Lambda Configuration

* Go to **Lambda Console**
* Function: `lambda-rdsconnect`
* Purpose: RDS database connections

✅ **Connect to RDS database**

1. Function `lambda-rdsconnect` is **not attached to a VPC**
2. Choose **Use an existing database**
3. RDS Database: `mydbinstance`

---

### ✅ Step 8: Lambda Function Code

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
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        if connection:
            connection.close()
```

---

### ✅ Step 9: Deploy and Test

1. Click **Deploy** in Lambda Console
2. Click **Test** → Create a test event
3. On success, you will see a message confirming database and table creation

---

### ✅ Step 10: Connect Your RDS Using External Tools

#### 🔹 A. MySQL Workbench

1. Open **MySQL Workbench** → Add new connection
2. Set:

   * Connection Name: `rds-test-db`
   * Hostname: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
   * Port: `3306`
   * Username: `admin`
   * Password: enter and store
3. Click **Test Connection**
4. ✅ Ensure RDS Security Group allows TCP 3306 from your IP

#### 🔹 B. Using EC2

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

Expected Output:

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

🎉 Done! You have successfully connected Lambda to RDS using Secrets Manager with proper IAM and Layer setup.
