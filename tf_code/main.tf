module "demo_sg" {
  source = "terraform-aws-modules/security-group/aws"
  version = "4.9.0"

  name        = local.name
  description = "Security group for LiveEO demo with open SSH access"
  vpc_id      = "vpc-0ca0a9bb3bd46bd08"

  tags        = local.tags
  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "ssh ports"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 8000
      to_port     = 8000
      protocol    = "tcp"
      description = "api ports"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_with_cidr_blocks = [
  {
    rule = "all-all"
  }
]

}

module "ec2-instance-liveEO-demo" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "4.0.0"

  name                        = local.name
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t2.micro"
  key_name                    = "demo"
  vpc_security_group_ids      = [module.demo_sg.security_group_id]
  tags                         = local.tags
}

resource "null_resource" "example_provisioner1" {
  triggers = {
    public_ip = module.ec2-instance-liveEO-demo.public_ip
  }

  connection {
    type  = "ssh"
    host  = module.ec2-instance-liveEO-demo.public_ip
    user  = local.ssh_user
    port  = local.ssh_port
    private_key = file(local.key_pair_path)
    agent = true
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p ~/app",
      "mkdir -p ~/test"
    ]
  }
  // copy our example script to the server
  provisioner "file" {
    source      = "../app"
    destination = "app"
  }

  provisioner "file" {
    source      = "../test"
    destination = "test"
  }

  // change permissions to executable and pipe its output into a new file
  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install docker -y",
      "sudo usermod -a -G docker ec2-user",
      "sudo systemctl start docker ",
      "sleep 60",
      "cd ~/test/test",
      "docker build -t test_container .",
      "cd ~/app/app",
      "docker build -t liveeo .",
      "docker run -d -p 8000:8000 liveeo",
    ]
  }

}
