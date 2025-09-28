resource "aws_db_subnet_group" "dbs_subnet" {
  name       = "main"
  subnet_ids = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]

  tags = {
    Name = "My DB subnet group for mood-tracker-app"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 10
  db_name              = "moodtracker"
  engine               = "postgres"
  engine_version       = "11.22-rds.20250508"          # latest free tier Postgres
  instance_class       = "db.t3.micro"
  username             = "adminpree73674"
  password             = "foobarbaz999"
  skip_final_snapshot  = true
  publicly_accessible  = false
}

