resource "aws_lambda_function" "ingester_lambda" {
    # filename = "${path.module}/../${var.lambda_name}.zip"
    filename = "${path.module}/../python.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "python.ingestion_handler"
    # handler = "${var.python_file_name}.ingestion_handler"
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
    environment {
      variables = {
        DB_USER = "project_user_7",
        DB_NAME = "totesys",
        DB_PORT = "5432",
        DB_HOST = "nc-data-eng-totesys-production.chpsczt8h1nu.eu-west-2.rds.amazonaws.com",
        DB_PASSWORD = "WRb2miiYPXX19TXr"
      }
    }
}

resource "aws_lambda_permission" "allow_eventbridge" {
    action         = "lambda:InvokeFunction"
    function_name  = aws_lambda_function.ingester_lambda.function_name
    principal      = "scheduler.amazonaws.com"
    source_arn     = aws_scheduler_schedule.ingester_schedule.arn
}