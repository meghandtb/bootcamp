# 🛠️ AWS Private Infrastructure with Terraform & CloudFormation

This project provisions a secure AWS infrastructure using **Terraform**, with a bonus implementation using **CloudFormation**. It includes:

- A VPC named `cyber-vpc-1`
- Two private subnets in different AZs (`eu-west-1a`, `eu-west-1b`)
- A security group allowing **only internal SSH traffic**
- Two EC2 instances (`node-a` and `node-b`) with **no public IPs**
- Remote state management using **S3 + DynamoDB**

---

## ✅ Prerequisites

- AWS CLI configured (`aws configure`)
- Terraform installed
- An SSH key pair created in AWS (for EC2 access)

---

## 🚀 Terraform Setup

### 1. Remote Backend Configuration

- **S3 bucket** was created via the AWS Console to store the Terraform state file:

![S3 bucket screenshot](https://github.com/user-attachments/assets/7859ffeb-6cc5-48a1-a00f-616e2afc6d42)

- **DynamoDB table** was created to enable state locking:

```bash
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-west-1
```

![image](https://github.com/user-attachments/assets/5c6ce314-5ac9-440d-8027-98fc023ac0ec)

2. Initialize Terraform
```
terraform init
```

3. Apply Infrastructure
```
terraform apply
```

4. Output Private IPs

After applying, the following private IPs were returned:
```
node_a_private_ip = "10.10.1.75"
node_b_private_ip = "10.10.2.107"
```

🔐 SSH Access (Internal Only)

A key pair was created via the AWS Console and used for SSH access:

![image](https://github.com/user-attachments/assets/fbe87c91-2e8a-473d-8a51-6580345066ee)

Since the instances are in private subnets, I used EC2 Instance Connect + Private IP to SSH in from one instance to another.

SSH from Node-a to Node-b:

![image](https://github.com/user-attachments/assets/2cc8e313-864b-4661-b98f-000dd98ed590)

SSH from Node-b to Node-a:

![image](https://github.com/user-attachments/assets/ec010c94-58dd-45f7-bb06-8bffc6e8165b)

🧹 Terraform Cleanup

To clean up the Terraform-managed infrastructure:
```
terraform destroy
```

📦 CloudFormation Stack Deployment

The same infrastructure was re-created using CloudFormation with this command:

```
aws cloudformation create-stack \
  --stack-name cyber-vpc-stack \
  --template-body file://infrastructure.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

![image](https://github.com/user-attachments/assets/ba37cb4f-d1e6-494f-8402-87610c327a4d)

Internal SSH Tests

Node-a to Node-b:


![image](https://github.com/user-attachments/assets/33514fc2-7e88-4121-9685-e9a163348715)

Node-b to Node-a:

![image](https://github.com/user-attachments/assets/b2625252-17eb-4f62-a758-8a7b30caf40b)

💭 Reflection
✅ What was easier with Terraform?

    Modular and reusable: Easier to split into main.tf, variables.tf, and outputs.tf

    Stateful infrastructure tracking: Terraform’s state file helps detect drift and simplifies updates

    Faster iteration: Changes apply faster than redeploying full CloudFormation stacks

🤔 What was easier with CloudFormation?

    Native AWS integration: Easier to view and manage resources directly in the CloudFormation console

    No extra tools needed beyond the AWS CLI/console

🛠️ What I'd improve

    Use modules in Terraform to improve structure and reuse

    Split the variables in the CloudFormation code similar to how it was done for Terraform, for better reusability

    Automate private key handling using user_data or AWS SSM parameters (instead of manual key copying)
