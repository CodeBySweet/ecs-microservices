variable "ecs_service_name" {
  type        = string
  description = "Name of the ECS service"
}

variable "cluster_id" {
  type        = string
  description = "ECS cluster ID or ARN"
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnet IDs"
}

variable "security_group_ids" {
  type        = list(string)
  description = "List of security group ID"
}

variable "image_main" {
  type        = string
  description = "Docker image URI"
}

variable "image_auth" {
  type        = string
  description = "Docker image URI"
}

variable "image_product" {
  type        = string
  description = "Docker image URI"
}

variable "image_user" {
  type        = string
  description = "Docker image URI"
}

variable "cpu" {
  type = string
}

variable "memory" {
  type = string
}

variable "execution_role_arn" {
  type        = string
  description = "ECS execution role arn"
}

variable "task_role_arn" {
  type        = string
  description = "ECS task role arn"
}

# variable "container_port" {
#   type        = number
#   description = "Task Definition Ports"
# }

variable "container_definitions_name" {
  type        = string
  description = "Container Definitions Name"
}

variable "task_family" {
  type        = string
  description = "Task Definition Family"
}

variable "desired_count" {
  type        = number
  description = "ECS Service Desired Count"
}

variable "alb_tg" {
  type        = string
  description = "ALB Target Group"
}

variable "cluster_name" {
  type        = string
  description = "ECS cluster name"
}

variable "region" {
  type        = string
  description = "AWS region"
}

variable "main_vpc_id" {
  type = string
}

variable "alb_sg_name" {
  type = string
}

variable "alb_name" {
  type = string
}