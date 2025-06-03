# Python Backend Testing (flask\_rds\_user\_api) - Step-by-Step Guide

This guide covers how to set up a backend API using Python Flask and connect it to an Amazon RDS MySQL database hosted on AWS.



<table style="width: 100%; margin-bottom: 20px;">
  <tr>
    <td align="center" style="padding: 10px; background-color: #e9f7f5; border-radius: 8px;">
      <img src="https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation/blob/b2d1845dd739a2479a3b68452c7750051b3cee6c/Python-backend-testing/images.png" width="1000%" style="border: 2px solid #ddd; border-radius: 10px;">
      <br><b> Python backend testing  architecture Project </b>
    </td>
  </tr>
</table>


---

## ✅ Step 1: Set Up Your RDS Database

1. Go to AWS Console → Search **RDS** → Click **Create database**
2. Choose:

   * **Standard create**
   * **Engine**: MySQL
   * **Template**: Free tier
3. Settings:

   * **DB Instance Identifier**: `mydbinstance`
   * **Master Username**: `admin`
   * **Master Password**: `******`
   * **Public access**: Yes
4. Click **Create database**

### Note your RDS credentials:

* Endpoint: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
* Username: `admin`
* Password: `******`

---

---

## ✅ Step 2: Create IAM Role for EC2

1. Open **IAM Console** → Click **Roles** → **Create Role**
2. Trusted entity type: **AWS service**
3. Use case: **EC2**
4. Attach policy: `AdministratorAccess`
5. Role name: `ec2-admin`
6. Click **Create role**

---

## ✅ Step 4: Launch and Configure EC2 Instance

1. Go to **EC2 Console** → Click **Launch Instance**
2. Set:

   * Name: `backend server`
   * AMI: **Amazon Linux 2 AMI (HVM), Kernel 5.10**
   * Instance type: `t2.micro`
   * Key pair: `my-key-pair`
   * Network settings: Allow all traffic
   * IAM Role: `ec2-admin`
   * Storage: Default 8 GiB
3. Click **Launch Instance**

---

## ✅ Step 5: Connect to RDS in MySQL Workbench

1. Open **MySQL Workbench**

2. Connect to your RDS database:

   * Endpoint: `mydbinstance.c0n8k0a0swtz.us-east-1.rds.amazonaws.com`
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

## ✅ Step 6: Deploy Flask Backend on EC2

### Connect to your EC2 instance:

```bash
sudo su -
yum install python3-pip -y
pip3 install flask mysql-connector-python
yum install git -y
git clone https://github.com/arumullayaswanth/AWS-Lambda-boto3-automation.git
cd 4.python-backend-testing
python3 app.py
```

### To run Flask in background:

nohup allows your app to continue running even after terminal disconnect:

```bash
nohup python3 app.py > flask.log 2>&1 &
tail -f flask.log
```

To check if the app is running:

```bash
ps aux | grep app.py
```

To stop it:

```bash
pkill -f app.py
```

---

✅ Step 7: Reconnect to EC2 backend server once again&#x20;

Now your application is running And don't Exit your application and take the new window and connect once again your EC2 backend server and run these commands again.

Open a **new terminal window** and SSH back into EC2:

```bash
ssh -i "your-key.pem" ec2-user@<EC2 Public IP>
sudo -i
```

---

## ✅ Step 8: API Methods and Testing

### Flask API Supports:

* `GET /users` → Fetch all users
* `GET /users/<id>` → Fetch single user by ID
* `POST /users/add` → Add a new user
* `PUT /users/update/<id>` → Update user
* `DELETE /users/delete/<id>` → Delete user

### Example `curl` Commands:  Run this commands in EC2  backend server

**GET all users:**

```bash
curl -X GET http://localhost:5000/users/1
```

**GET single user:**

```bash
curl -X GET http://localhost:5000/users
```

**POST - Add user:**

```bash
curl -X POST http://localhost:5000/users/add \
     -H "Content-Type: application/json" \
     -d '{"name":"John Doe", "email":"john@example.com"}'
```

**PUT - Update user:**

```bash
curl -X PUT http://localhost:5000/users/update/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated", "email": "john.updated@example.com"}'
```

**DELETE - Remove user:**

```bash
curl -X DELETE http://localhost:5000/users/delete/1
```

---

## ✅ Step 9: Postman Testing (Optional)

 Go to Google and search postman tool this is an alternate tool to test

   Go to [https://postman.com](https://postman.com)

1. Create a **new request**

2. Use your **EC2 public IP** in place of `localhost`, e.g.

```bash
GET http://<EC2-Public-IP>:5000/users
```

4. Set headers to `Content-Type: application/json` for POST/PUT

###

---

## ✅ Summary

* You now have a Flask backend running on EC2
* It connects to RDS MySQL and supports CRUD APIs for user management
* You can test with `curl` or Postman
* Run it in the background using `nohup`

🎉 You're ready for backend development and testing!
