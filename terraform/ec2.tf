resource "aws_instance" "app_server" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t3.micro"
  subnet_id = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.allow_tls.id]

  tags = {
    Name = "My mood tracker app instance"
  }
}