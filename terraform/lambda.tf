resource "aws_lambda_function" "ingester_lambda" {
    filename = "${path.module}/../${var.lambda_name}.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "${var.python_file_name}.ingestion_handler"
}

# resource "aws_lambda_permission" "allow_s3" { EVENTBRIDGE MAYBE??? 
#   action         = "lambda:InvokeFunction"
#   function_name  = aws_lambda_function.ingester_lambda.function_name
#   principal      = "s3.amazonaws.com"
#   source_arn     = aws_s3_bucket.{JSON_bucket}.arn
#   source_account = data.aws_caller_identity.current.account_id
# }