## ✅ NGINX\_Load\_Balancer\_Steps.md

---

## ✅ Step 1: Setup Environment

You need **three EC2 instances**:

1. **NGINX Load Balancer Server** (in a **Public Subnet**) — to receive and route traffic.
2. **Application Server 1** (in a **Private Subnet**) — to serve content.
3. **Application Server 2** (in a **Private Subnet**) — to serve content.

### 🔧 Network Setup:

* **Public Subnet** for the Load Balancer: This allows it to receive external HTTP traffic from the internet.
* **Private Subnet** for Application Servers: Not exposed to the public internet, increasing security.
* All instances should be in the **same VPC** to allow communication between Load Balancer and backend servers.

### 🚀 Creating EC2 Instances

#### 🛠 Create Load Balancer Server (Public Subnet)

1. Go to **EC2 → Launch Instance**.
2. Choose **Amazon Linux 2 AMI**.
3. Instance Type: **t2.micro** (Free Tier).
4. Configure Instance:

   * Subnet: Select your **Public Subnet**.
   * Auto-assign Public IP: **Enable**.
5. Add Storage: Keep default (8 GB).
6. Security Group:

   * Allow:

     * **HTTP (port 80)** from `0.0.0.0/0`
     * **SSH (port 22)** from your IP
7. Launch with key pair.
8. Name it: `nginx-load-balancer`.

---

#### 🛠 Create Application Server (Private Subnet)

1. Go to **EC2 → Launch Instance**.
2. Choose **Amazon Linux 2 AMI**.
3. Instance Type: **t2.micro** (Free Tier).
4. Configure Instance:

   * Subnet: Select your **Private Subnet**.
   * Auto-assign Public IP: **Disable**.
5. Add Storage: Keep default.
6. Security Group:

   * Allow:

     * **HTTP (port 80)** from **Security Group of Load Balancer**
     * **SSH (port 22)** from Load Balancer’s Security Group or Bastion Host
7. Launch with key pair.
8. Name it: `app-server-private`.

---

## ✅ Step 2: Install Application on Backend Servers

#### 📦 Install Apache HTTP Server

Run the following commands **on both application servers**:

```bash
sudo yum install httpd -y
sudo systemctl enable httpd
sudo systemctl start httpd
```

#### 📝 Create a Test Web Page

* On **Application Server 1**:

```bash
echo "This is Private Server 1" | sudo tee /var/www/html/index.html
```

* On **Application Server 2**:

```bash
echo "This is Private Server 2" | sudo tee /var/www/html/index.html
```

#### ✅ Verify:

From the Load Balancer server, run:

```bash
curl http://<PRIVATE_IP_APP_SERVER_1>
curl http://<PRIVATE_IP_APP_SERVER_2>
```

You should see the respective test messages.

---

## ✅ Step 3: Install NGINX on the Load Balancer Server

#### 🛠 Install NGINX

```bash
sudo amazon-linux-extras enable nginx1
sudo yum clean metadata
sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

```

#### 🔍 Verify Installation

```bash
systemctl status nginx
```

Should show `active (running)`.

---

## ✅ Step 4: Configure NGINX Load Balancer

#### 📁 Create Configuration File

```bash
sudo vi /etc/nginx/conf.d/loadbalancer.conf
```

#### 🧾 Add the Following Configuration:

```nginx
upstream backend_servers {
    server 172.31.45.10;  # Application Server 1 Private IP
    server 172.31.45.11;  # Application Server 2 Private IP
}

server {
    listen 80;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

> ⚠️ Replace the IPs with your actual private IPs.

#### 💾 Save and Exit:

Press `ESC`, type `:wq!`, and press Enter.

---

## ✅ Step 5: Validate and Restart NGINX

#### 🧪 Validate Configuration:

```bash
sudo nginx -t
```

#### 🔁 Reload NGINX:

```bash
sudo systemctl reload nginx
```

---

## ✅ Step 6: Test Load Balancer

Open your browser and visit:

```http
http://<LOAD_BALANCER_PUBLIC_IP>
```

#### 🔄 Expected Output:

* Refresh the page multiple times.
* You should see alternating messages:

  * "This is Private Server 1"
  * "This is Private Server 2"

🎉 Your NGINX Load Balancer is now successfully distributing traffic across two backend servers!



# Nginx Installation and Configuration Command History

```bash
sudo yum install httpd -y
sudo systemctl enable httpd

sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
systemctl status nginx

sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

sudo amazon-linux-extras enable nginx1
sudo yum clean metadata
sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
systemctl status nginx

sudo vi /etc/nginx/conf.d/loadbalancer.conf
sudo nginx -t
sudo systemctl reload nginx

sudo cat /etc/nginx/nginx.conf
sudo cat /etc/nginx/conf.d/default.conf
vim /etc/nginx/conf.d/default.conf

sudo systemctl restart nginx

sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
sudo cat /etc/nginx/conf.d/loadbalancer.conf
sudo nginx -t
sudo systemctl reload nginx

history
