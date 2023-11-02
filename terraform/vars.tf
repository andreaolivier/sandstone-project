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