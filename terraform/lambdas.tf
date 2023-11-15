# Ingestion lambda

resource "aws_lambda_function" "ingester_lambda" {
    filename = "${path.module}/../ingestion_handler.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "ingestion_handler.ingestion_handler"
    layers = [aws_lambda_layer_version.automated_layer.arn]

    timeout = 60
    environment {
      variables = {
      DB_USER = var.db_user,
      DB_NAME = var.db_name,
      DB_PORT = var.db_port,
      DB_HOST = var.db_host,
      DB_PASSWORD = var.db_password
    }
}
}

resource "aws_lambda_permission" "allow_eventbridge" {
    action         = "lambda:InvokeFunction"
    function_name  = aws_lambda_function.ingester_lambda.function_name
    principal      = "scheduler.amazonaws.com"
    source_arn     = aws_scheduler_schedule.ingester_schedule.arn
}

# Process lambda

resource "aws_lambda_function" "process_lambda" {
    filename = "${path.module}/../processing_handler.zip"
    function_name = "${var.process_lambda_name}"
    role = aws_iam_role.process_role.arn
    runtime = "python3.11"
    handler = "processing_handler.processing_handler"
    layers = [aws_lambda_layer_version.automated_layer.arn, 
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:3"]
    timeout = 60
    environment {
      variables = {
      DB_USER = var.db_user,
      DB_NAME = var.db_name,
      DB_PORT = var.db_port,
      DB_HOST = var.db_host,
      DB_PASSWORD = var.db_password
    }
  }
}

resource "aws_lambda_permission" "allow_put_object_event" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.process_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.ingested_data_bucket.arn
}

# Upload lambda

resource "aws_lambda_function" "upload_lambda" {
    filename = "${path.module}/../upload.zip"
    function_name = "${var.upload_lambda}"
    role = aws_iam_role.upload_role.arn
    runtime = "python3.11"
    handler = "upload.lambda_handler"
    layers = [aws_lambda_layer_version.automated_layer.arn, 
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:3"]
    timeout = 60
    environment {
      variables = {
      DW_USER = var.dw_user,
      DW_NAME = var.dw_name,
      DW_PORT = var.dw_port,
      DW_HOST = var.dw_host,
      DW_PASSWORD = var.dw_password
    }
  }
}

resource "aws_lambda_permission" "parquet_object_added" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.upload_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.processed_data_bucket.arn
  depends_on = [ aws_cloudwatch_log_group.upload_lambda ]
}