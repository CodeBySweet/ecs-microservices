data "aws_security_group" "alb_sg" {
  name = var.alb_sg_name
}

data "aws_lb" "app" {
  name = var.alb_name
}

data "aws_lb_listener" "http" {
  load_balancer_arn = data.aws_lb.app.arn
  port              = 80
}

data "aws_service_discovery_dns_namespace" "my_namespace" {
  name = "my-namespace.local"
  type = "DNS_PRIVATE"
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.cluster_name}"
  retention_in_days = 7
}

resource "aws_security_group" "ecs_service_sg" {
  name        = "${var.cluster_name}-ecs-sg"
  description = "Security group for all ECS services"
  vpc_id      = var.main_vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "allow_alb_to_ecs_range" {
  type                     = "ingress"
  from_port                = 3001
  to_port                  = 3004
  protocol                 = "tcp"
  source_security_group_id = data.aws_security_group.alb_sg.id
  security_group_id        = aws_security_group.ecs_service_sg.id
  description              = "Allow ALB to access ECS services"
}

resource "aws_security_group_rule" "allow_ecs_to_ecs" {
  type                     = "ingress"
  from_port                = 3001
  to_port                  = 3004
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.ecs_service_sg.id
  security_group_id        = aws_security_group.ecs_service_sg.id
  description              = "Allow ECS services to communicate with each other"
}

# Target Groups
resource "aws_lb_target_group" "main" {
  name        = "${var.cluster_name}-main-tg"
  port        = 3004
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.main_vpc_id

  health_check {
    path                = "/main/health"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group" "auth" {
  name        = "${var.cluster_name}-auth-tg"
  port        = 3003
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.main_vpc_id

  health_check {
    path                = "/auth/health"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group" "product" {
  name        = "${var.cluster_name}-product-tg"
  port        = 3001
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.main_vpc_id

  health_check {
    path                = "/product/health"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group" "user" {
  name        = "${var.cluster_name}-user-tg"
  port        = 3002
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.main_vpc_id

  health_check {
    path                = "/user/health"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_ecs_task_definition" "main" {
  family                   = "${var.cluster_name}-main"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = "main"
      image     = var.image_main
      portMappings = [
        {
          containerPort = 3004
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "main"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "auth" {
  family                   = "${var.cluster_name}-auth"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = "auth"
      image     = var.image_auth
      portMappings = [
        {
          containerPort = 3003
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "auth"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "product" {
  family                   = "${var.cluster_name}-product"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = "product"
      image     = var.image_product
      portMappings = [
        {
          containerPort = 3001
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "product"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "user" {
  family                   = "${var.cluster_name}-user"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = "user"
      image     = var.image_user
      portMappings = [
        {
          containerPort = 3002
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "user"
        }
      }
    }
  ])
}

# ECS Services
resource "aws_ecs_service" "main" {
  name            = "${var.cluster_name}-main"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  enable_execute_command = true

  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = "main"
    container_port   = 3004
  }

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.main.arn
  }

  depends_on = [aws_lb_target_group.main, aws_lb_listener_rule.main]
}

resource "aws_ecs_service" "auth" {
  name            = "${var.cluster_name}-auth"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.auth.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  enable_execute_command = true

  load_balancer {
    target_group_arn = aws_lb_target_group.auth.arn
    container_name   = "auth"
    container_port   = 3003
  }

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.auth.arn
  }

  depends_on = [aws_lb_target_group.auth, aws_lb_listener_rule.auth]
}

resource "aws_ecs_service" "product" {
  name            = "${var.cluster_name}-product"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.product.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  enable_execute_command = true

  load_balancer {
    target_group_arn = aws_lb_target_group.product.arn
    container_name   = "product"
    container_port   = 3001
  }

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.product.arn
  }


  depends_on = [aws_lb_target_group.product, aws_lb_listener_rule.product]
}


resource "aws_ecs_service" "user" {
  name            = "${var.cluster_name}-user"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.user.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  enable_execute_command =   true

  load_balancer {
    target_group_arn = aws_lb_target_group.user.arn
    container_name   = "user"
    container_port   = 3002
  }

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.user.arn
  }

  depends_on = [aws_lb_target_group.user, aws_lb_listener_rule.user]
}


resource "aws_lb_listener_rule" "main" {
  listener_arn = data.aws_lb_listener.http.arn
  priority     = 90

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }

  condition {
    path_pattern {
      values = ["/"]
    }
  }
}

resource "aws_lb_listener_rule" "auth" {
  listener_arn = data.aws_lb_listener.http.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.auth.arn
  }

  condition {
    path_pattern {
      values = ["/auth*", "/login", "/auth/internal-test"]
    }
  }
}

resource "aws_lb_listener_rule" "product" {
  listener_arn = data.aws_lb_listener.http.arn
  priority     = 110

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.product.arn
  }

  condition {
    path_pattern {
      values = ["/product*", "/product/internal-test"]
    }
  }
}

resource "aws_lb_listener_rule" "user" {
  listener_arn = data.aws_lb_listener.http.arn
  priority     = 120

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.user.arn
  }

  condition {
    path_pattern {
      values = ["/user*", "/user/internal-test"]
    }
  }
}

resource "aws_service_discovery_service" "main" {
  name = "main"

  dns_config {
    namespace_id = data.aws_service_discovery_dns_namespace.my_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_service_discovery_service" "auth" {
  name = "auth"

  dns_config {
    namespace_id = data.aws_service_discovery_dns_namespace.my_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_service_discovery_service" "product" {
  name = "product"

  dns_config {
    namespace_id = data.aws_service_discovery_dns_namespace.my_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}


resource "aws_service_discovery_service" "user" {
  name = "user"

  dns_config {
    namespace_id = data.aws_service_discovery_dns_namespace.my_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}