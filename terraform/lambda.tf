resource "aws_lambda_layer_version" "lambda_layer" {
    filename   = "${path.module}/../python.zip"
    layer_name = "pandas_module_layer"
    compatible_runtimes = ["python3.11"]
}

resource "aws_lambda_function" "ingester_lambda" {
    # filename = "${path.module}/../${var.lambda_name}.zip"
    filename = "${path.module}/../ingester.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "ingester.ingestion_handler"
    # handler = "${var.python_file_name}.ingestion_handler"
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
    # environment {
    #   # variables = {
    #   # DB_USER = var.DB_USER,
    #   # DB_NAME = var.DB_NAME,
    #   # DB_PORT = var.DB_PORT,
    #   # DB_HOST = var.DB_HOST,
    #   # DB_PASSWORD = var.DB_PASSWORD
    # }
    depends_on = [ aws_lambda_layer_version.lambda_layer ]
  }

resource "aws_lambda_permission" "allow_eventbridge" {
    action         = "lambda:InvokeFunction"
    function_name  = aws_lambda_function.ingester_lambda.function_name
    principal      = "scheduler.amazonaws.com"
    source_arn     = aws_scheduler_schedule.ingester_schedule.arn
}