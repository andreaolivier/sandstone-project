resource "aws_lambda_function" "process_lambda" {
    filename = "${path.module}/../processing_handler.zip"
    function_name = "${var.process_lambda_name}"
    role = aws_iam_role.process_role.arn
    runtime = "python3.11"
    handler = "processing_handler.processing_handler"
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
}

resource "aws_lambda_permission" "allow_s3" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.process_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.processed_data_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}