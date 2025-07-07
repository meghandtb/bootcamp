This project provisions secure AWS infrastructure using Terraform, with a bonus implementation in CloudFormation. It includes:

    A VPC named cyber-vpc-1
    Two private subnets in different AZs (eu-west-1a, eu-west-1b)
    A security group allowing only internal SSH between the subnets
    Two EC2 instances (node-a and node-b) in private subnets (no public IPs)
    Remote state management using S3 + DynamoDB

🚀 Terraform Instructions
✅ Prerequisites

    AWS CLI configured (aws configure)
    Terraform installed
    SSH key pair created in AWS

🏗️ Provision Infrastructure

🚀 Usage

    Set up Backend

    Created an S3 bucket for state file throught the AWS console.

![image](https://github.com/user-attachments/assets/7859ffeb-6cc5-48a1-a00f-616e2afc6d42)


    Created a DynamoDB table for state locking as follows:

aws dynamodb create-table
--table-name terraform-locks
--attribute-definitions AttributeName=LockID,AttributeType=S
--key-schema AttributeName=LockID,KeyType=HASH
--billing-mode PAY_PER_REQUEST
--region eu-west-1

![image](https://github.com/user-attachments/assets/5c6ce314-5ac9-440d-8027-98fc023ac0ec)


    Initialize Terraform

terraform init

    Apply Infrastructure

terraform apply

    Get Private IPs

After terraform apply, i got the following private IPs:

node_a_private_ip = "10.10.1.75" node_b_private_ip = "10.10.2.107"

🔐 SSH Access

In order to establish SSH connection I performed the following steps:

Created a SSH key through the AWS console and used it for SSH access:

![image](https://github.com/user-attachments/assets/fbe87c91-2e8a-473d-8a51-6580345066ee)


Since the created instances have private IPs, I used EC2 Instance Connect which required an endpoint in order to establish connection.

SSH from Node-b to Node-a:

![image](https://github.com/user-attachments/assets/ec010c94-58dd-45f7-bb06-8bffc6e8165b)


SSH from Node-a to Node-b:

![image](https://github.com/user-attachments/assets/2cc8e313-864b-4661-b98f-000dd98ed590)


Terraform Infrastructure cleanup

Ran terraform destroy in order to clean up the terraform infrastructure, so it can be deployed trough CloudFormation.

Cloud Formation Infrastructure:

Create the CloudFormation stack as follows:

aws cloudformation create-stack \                       
  --stack-name cyber-vpc-stack \
  --template-body file://infrastructure.yaml \
  --capabilities CAPABILITY_NAMED_IAM

![image](https://github.com/user-attachments/assets/ba37cb4f-d1e6-494f-8402-87610c327a4d)

SSH from Node-a to Node-b:

![image](https://github.com/user-attachments/assets/33514fc2-7e88-4121-9685-e9a163348715)

SSH from Node-b to Node-a:

![image](https://github.com/user-attachments/assets/b2625252-17eb-4f62-a758-8a7b30caf40b)



