resource "aws_vpc" "vpc_main" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "vpc"
  }
}
#creating two subnets to which the vpc belongs
resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.vpc_main.id   #to which vpc it belongs
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true   # <- This is necessary
  tags = {
    Name = "app subnet"
  }
}
resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.vpc_main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.vpc_main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1b"
}
