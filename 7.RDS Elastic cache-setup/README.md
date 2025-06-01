# AWS RDS + ElastiCache (Redis) + EC2 Setup Guide


<table style="width: 100%; margin-bottom: 20px;">
  <tr>
    <td align="center" style="padding: 10px; background-color: #e9f7f5; border-radius: 8px;">
      <img src="https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation-project/blob/ef852a6cb9c8f636a6e57c360b0ec6f33c5b057e/7.RDS%20Elastic%20cache-setup/rds_elastic_cache%20images.png" width="1000%" style="border: 2px solid #ddd; border-radius: 10px;">
      <br><b> AWS RDS + ElastiCache (Redis) + EC2 Setup Guide </b>
    </td>
  </tr>
</table>

# AWS RDS and ElastiCache Setup with Python Cache Integration
 
This guide provides detailed steps to set up an AWS environment with RDS (MySQL), ElastiCache (Redis), and EC2 for backend caching operations using Python.

---

## ✅ Step 1: Set Up Your RDS Database

1. Go to **AWS Console** → Search **RDS** → Dashboard → Click **Create database**

2. Choose:
   - Database creation method: **Standard create**
   - Engine options: **MySQL**
   - Templates: **Free tier**

3. Configure settings:
   - DB Instance Identifier: `mydbinstance`
   - Master Username: `admin`
   - Master Password: `******`
   - Public access: **No**

4. Click **Create database**

5. Note your RDS credentials:  
   - Endpoint: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`  
   - Username: `admin`  
   - Password: `******`

---

## ✅ Step 2: Create an Amazon ElastiCache Cluster

1. Go to **RDS** → Select `mydbinstance` database → Click **Actions** → Click **Create ElastiCache cluster**

2. ElastiCache cluster configuration:
   - Cluster type: **Redis OSS**
   - Deployment option: **Serverless cache**

3. Cache settings:
   - Name: `dev`

4. Click **Create ElastiCache cluster**

---

## ✅ Step 3: Verify ElastiCache Cluster Creation

1. Go to **ElastiCache** in AWS Console  
2. Select **Redis OSS Caches**  

Verify if the cluster named `dev` is created.

### Save Redis Credentials:
- **Endpoint**: `dev-l6ap1d.serverless.use1.cache.amazonaws.com:6379`

---

## ✅ Step 4: Create IAM Role for EC2

1. Open **IAM Console** → Click **Roles** → **Create Role**

2. Configure:
   - Trusted entity type: **AWS service**
   - Use case: **EC2**
   - Attach policy: **AdministratorAccess**
   - Role name: `ec2-admin`

3. Click **Create role**

---

## ✅ Step 5: Launch an EC2 Instance for Backend Server

1. Go to **EC2 Console** → Click **Launch Instance**

2. Set:
   - Name: `backend server`
   - AMI: **Amazon Linux 2 AMI (HVM), Kernel 5.10**
   - Instance type: **t2.micro**
   - Key pair: `my-key-pair`
   - Network settings: Allow all traffic, default
   - IAM Role: `ec2-admin`
   - Storage: Default 8 GiB

3. Click **Launch Instance**

> **Note:** EC2, VPC, and RDS should all be in the same network and security group to communicate.

---

## ✅ Step 6: Connect to your EC2 Backend Server Instance and Install Dependencies

1. SSH into your EC2 instance

2. Run these commands to install dependencies:

```bash
sudo -i
yum install mariadb-server -y
mysql --version
sudo yum install python3-pip -y
pip3 install pymysql redis
```

---

## ✅ Step 7: Connect to Your RDS Database from EC2

```bash
mysql -h <rds-endpoint> -u admin -p
```

Example:

```bash
mysql -h database-1.c0n8k0a0swtz.us-east-1.rds.amazonaws.com -u admin -p
```

---

## ✅ Step 8: Create Database and Table with Sample Data

Run these SQL commands inside MySQL shell:

```sql
CREATE DATABASE test;
USE test;

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100)
);
```

### Insert Sample Data:

```sql
INSERT INTO users (user_id, first_name, last_name, email)
VALUES 
('12345', 'John', 'Doe', 'john.doe@example.com'),
('12346', 'Alice', 'Smith', 'alice.smith@example.com'),
('12347', 'Bob', 'Johnson', 'bob.johnson@example.com'),
('12348', 'Emily', 'Williams', 'emily.williams@example.com');
```
---


## ✅ Step 9: Create Your Python Script on EC2 to Integrate RDS and ElastiCache

1. Open a new terminal tab connected to your EC2 instance One more time

2. Create a new Python file:

```bash
vim rds_elastic_cache_main.py
```

3. Paste the following Python code:

```python
# Import necessary libraries
import pymysql        # For connecting to MySQL (RDS)
import redis          # For interacting with Redis (ElastiCache)
import json           # For encoding/decoding cached data
import sys            # To handle command-line arguments

# 🔧 Redis configuration (ElastiCache endpoint)
redis_client = redis.Redis(
    host='dev-l6ap1d.serverless.use1.cache.amazonaws.com',
    port=6379,
    ssl=True,
    decode_responses=True,
    socket_timeout=5
)

# 🔧 RDS (MySQL) configuration
RDS_HOST = 'database-1.c0n8k0a0swtz.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = '9959148343'
RDS_DB_NAME = 'test'
TABLE_NAME = 'users'

def fetch_data_from_rds():
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME
        )
        print("🔗 Connected to RDS")

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 10;")
            rows = cursor.fetchall()
            return rows

    except Exception as e:
        print("❌ RDS Error:", e)
        return None

    finally:
        if 'connection' in locals():
            connection.close()

def main():
    cache_key = 'cached_table_data'
    bypass_cache = "--refresh" in sys.argv

    if not bypass_cache:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            print("✅ Fetched from Redis cache:")
            print(json.loads(cached_data))
            return

    print("⚙️ No cache found or refresh requested. Fetching from RDS...")
    data = fetch_data_from_rds()

    if data:
        redis_client.set(cache_key, json.dumps(data), ex=90)
        print("📦 Cached in Redis:")
        print(data)
    else:
        print("⚠️ No data fetched from RDS.")

if __name__ == "__main__":
    main()
```

4. Save and exit (`:wq` in vim).

---

## ✅ Step 10: Run Your Python Script

```bash
python3 rds_elastic_cache_main.py
```

Re-run to confirm Redis caching:

```bash
python3 rds_elastic_cache_main.py
```

- The **first run** fetches data from RDS and caches it.
- Run the script **again** within 90 seconds and it will fetch data from Redis cache.

To force refresh cache and fetch fresh data from RDS:

```bash
python3 rds_elastic_cache_main.py --refresh
```

---

## ✅ Step 11: Add More Records to Test Cache Expiry

Add a new record:

```sql
INSERT INTO users (user_id, first_name, last_name, email)
VALUES ('12349', 'Michael', 'Brown', 'michael.brown@example.com');
```

Immediately run the script (cache will not reflect the new entry):

```bash
python3 rds_elastic_cache_main.py
```

After 90 seconds (cache expiration), re-run with refresh:

```bash
python3 rds_elastic_cache_main.py --refresh
```

Now the new record will be included.

---

## Notes:

- Cache expiry is set to 90 seconds.
- New records added within 90 seconds will **not** appear until cache expires.
- After 90 seconds, the cache refreshes and fetches new data from RDS.

---

# You're all set! 🚀

