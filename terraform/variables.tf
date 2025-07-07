variable "vpc_cidr" {
  default = "10.10.0.0/16"
}

variable "subnet_a_cidr" {
  default = "10.10.1.0/24"
}

variable "subnet_b_cidr" {
  default = "10.10.2.0/24"
}

variable "availability_zone_a" {
  default = "eu-west-1a"
}

variable "availability_zone_b" {
  default = "eu-west-1b"
}
