# Create a VPC
resource "aws_vpc" "cyber-vpc-1" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "cyber-vpc-1"
  }
}

resource "aws_subnet" "subnet-a" {
  vpc_id     = aws_vpc.cyber-vpc-1.id
  cidr_block = var.subnet_a_cidr
  availability_zone = var.availability_zone_a

  tags = {
    Name = "subnet-a"
  }
}

resource "aws_subnet" "subnet-b" {
  vpc_id     = aws_vpc.cyber-vpc-1.id
  cidr_block = var.subnet_b_cidr
  availability_zone = var.availability_zone_b

  tags = {
    Name = "subnet-b"
  }
}

resource "aws_security_group" "mutual-ssh-1" {
  name        = "mutual-ssh-1"
  description = "Allow mutual ssh"
  vpc_id      = aws_vpc.cyber-vpc-1.id

  tags = {
    Name = "mutual-ssh-1"
  }

  ingress {
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = [var.subnet_a_cidr, var.subnet_b_cidr]
    description      = "Allow ssh on inbound rules"
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "Allow all on outbound rules"
  }
}

resource "aws_instance" "node-a" {
  ami           = "ami-0db1de538d84beea0"
  instance_type = "t3.micro"
  subnet_id                   = aws_subnet.subnet-a.id
  vpc_security_group_ids      = [aws_security_group.mutual-ssh-1.id]
  associate_public_ip_address = false
  key_name                    = "terraform-key"

  tags = {
    Name = "node-a"
  }
}

resource "aws_instance" "node-b" {
  ami           = "ami-0db1de538d84beea0"
  instance_type = "t3.micro"
  subnet_id                   = aws_subnet.subnet-b.id
  vpc_security_group_ids      = [aws_security_group.mutual-ssh-1.id]
  associate_public_ip_address = false
  key_name                    = "terraform-key"

  tags = {
    Name = "node-b"
  }
}

terraform {
  backend "s3" {
    bucket         = "terraform-bucket-assignment3-2734"
    key            = "episode2/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
