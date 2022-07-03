locals {
  name   = "liveEO_demo"
  region = "us-east-1"
  key_pair_path = "~/.ssh/demo.pem"
  ssh_user = "ec2-user"
  ssh_port = "22"

  user_data = <<-EOT
  #!/bin/bash
  echo "Hello Terraform!"
  EOT

  tags = {
    Owner       = "Sai"
    Environment = "demo"
    Project     = "LiveEO"
  }
}
