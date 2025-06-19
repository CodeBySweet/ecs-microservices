data "aws_security_group" "alb_sg" {
  name = var.alb_sg_name
}

############## Security Group#########
resource "aws_security_group" "ecs_service_sg" {
  name        = "${var.ecs_service_name}-sg"
  description = "Security group for ECS service exposing port ${var.container_port}"
  vpc_id      = var.main_vpc_id

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.ecs_service_name}-sg"
  }
}

resource "aws_security_group_rule" "allow_alb_to_ecs" {
  type                     = "ingress"
  from_port                = var.container_port
  to_port                  = var.container_port
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ecs_service_sg.id
  source_security_group_id = data.aws_security_group.alb_sg.id
  description              = "Allow traffic from ALB"
}

############## ECS Service ########
resource "aws_ecs_service" "main" {
  name                              = var.ecs_service_name
  cluster                           = var.cluster_id
  task_definition                   = aws_ecs_task_definition.main.arn
  desired_count                     = var.desired_count
  launch_type                       = "FARGATE"
  scheduling_strategy               = "REPLICA"
  health_check_grace_period_seconds = 60

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.alb_tg
    container_name   = var.container_definitions_name
    container_port   = var.container_port
  }

}

########### Cloudwatch Log ######
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.cluster_name}"
  retention_in_days = 7
}

########### Task definition #########
resource "aws_ecs_task_definition" "main" {
  family                   = var.task_family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = var.container_definitions_name
      image     = var.image
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/${var.cluster_name}"
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  depends_on = [aws_cloudwatch_log_group.ecs_logs]
}
