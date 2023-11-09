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