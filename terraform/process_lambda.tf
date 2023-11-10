resource "aws_lambda_function" "process_lambda" {
    filename = "${path.module}/../processing_handler.zip"
    function_name = "${var.process_lambda_name}"
    role = aws_iam_role.process_role.arn
    runtime = "python3.11"
    handler = "processing_handler.processing_handler"
    layers = ["arn:aws:lambda:eu-west-2:572843110802:layer:updated_layer:1", 
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