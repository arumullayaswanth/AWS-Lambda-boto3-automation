
# Connecting to a Private EC2 Instance Using AWS Session Manager

## 1. Create an IAM Role with `AmazonSSMManagedInstanceCore`

Before connecting to a private EC2 instance via Session Manager, create an IAM role that allows SSM access.

### Steps:
1. Open the **IAM Console**.
2. Go to **Roles** > **Create Role**.
3. Select **EC2** as the trusted entity.
4. Attach the `AmazonSSMManagedInstanceCore` policy.
5. Name the role (e.g., `ec2_ssm`) and click **Create Role**.

---

## 2. Launch a Public EC2 Instance

This instance acts as a jump box to prepare the AMI.

### Steps:
1. Open the **EC2 Console** and click **Launch Instance**.
2. Choose **Amazon Linux 2**, instance type `t2.micro`.
3. **Create a security group** that allows:
   - SSH (Port 22)
   - HTTP (Port 80)
   - HTTPS (Port 443)
4. Under **Advanced Details**, attach the IAM role `ec2_ssm`.
5. Click **Launch Instance**.

---

## 3. Connect to the Public EC2 Instance and Install SSM Agent

### Steps:
1. Use **EC2 Instance Connect** to SSH into the instance.
2. Switch to root:
   ```bash
   sudo su -
   ```
3. Update and install the SSM Agent:
   ```bash
   sudo dnf update -y
   sudo dnf install amazon-ssm-agent -y
   sudo systemctl start amazon-ssm-agent
   sudo systemctl enable amazon-ssm-agent
   ```
4. Verify the agent:
   ```bash
   sudo systemctl status amazon-ssm-agent
   ```

---

## 4. Create an Amazon Machine Image (AMI)

### Steps:
1. Go to the **EC2 Console** > select your instance.
2. Click **Actions** > **Image and templates** > **Create image**.
3. Name the image (e.g., `ssm_session_manager_img`) and create it.
4. Wait until the AMI status is **Available**.

---

## 5. Launch the Private EC2 Instance

### Steps:
1. Go to **AMIs** and select the custom AMI created earlier.
2. Click **Launch instance from AMI**.
3. Choose instance type `t2.micro`.
4. Under **IAM instance profile**, choose `ec2_ssm`.
5. Select a **Private Subnet** (ensure no public IP).
6. Launch the instance.

---

## 6. Create VPC Endpoints for SSM

These endpoints allow private EC2 to communicate with SSM without internet.

### Steps:
1. Open the **VPC Console** > **Endpoints** > **Create Endpoint**.
2. Create these **Interface Endpoints**:
   - `com.amazonaws.<region>.ssm`
   - `com.amazonaws.<region>.ssmmessages`
   - `com.amazonaws.<region>.ec2messages`
3. For each:
   - Select your VPC.
   - Choose private subnets.
   - Attach an appropriate security group.
4. Click **Create Endpoint**.

---

## 7. Connect to the Private EC2 Instance

### Option 1: Via Systems Manager Console
1. Go to **Systems Manager** > **Session Manager**.
2. Click **Start Session**, select your instance, and click **Start Session**.

### Option 2: Via EC2 Console
1. Go to **EC2 Console** > **Instances**.
2. Select the private instance.
3. Click **Connect** > **Session Manager** > **Connect**.

### Verify:
```bash
sudo systemctl status amazon-ssm-agent
```

---

## ✅ Conclusion

You’ve successfully set up a secure way to connect to a private EC2 instance using AWS Session Manager, with no need for public IPs or bastion hosts.
