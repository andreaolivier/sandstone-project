resource "aws_cloudwatch_log_group" "ingester_lambda" {
  name = "/aws/lambda/${var.lambda_name}"
}

resource "aws_cloudwatch_log_group" "process_lambda" {
  name = "/aws/lambda/${var.process_lambda_name}"
}

resource "aws_cloudwatch_log_group" "upload_lambda" {
  name = "/aws/lambda/${var.upload_lambda}"
}