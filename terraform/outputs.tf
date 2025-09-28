output "db_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "app_server_ip" {
  value = aws_instance.app_server.public_ip
}
