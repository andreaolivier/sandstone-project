variable "python_file_name" {
    type = string
    default = "ingester"
}

variable "lambda_name" {
    type = string
    default = "ingestion_handler"
}

variable "ingester_scheduler_name" {
    type = string
    default = "ingestion_scheduler"
}

variable "process_file_name" {
    type = string
    default = "processing_handler"
}

variable "process_lambda_name" {
    type = string
    default = "processing_handler"
}

variable "upload_lambda" {
    type = string
    default = "lambda_handler"
}

variable "db_user" {
    type = string
}

variable "db_name" {
    type = string
}
variable "db_port" {
    type = string
}
variable "db_host" {
    type = string
}
variable "db_password" {
    type = string
}

variable "dw_user" {
    type = string
}

variable "dw_name" {
    type = string
}
variable "dw_port" {
    type = string
}
variable "dw_host" {
    type = string
}
variable "dw_password" {
    type = string
}
