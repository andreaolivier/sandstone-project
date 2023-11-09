resource "aws_lambda_function" "process_lambda" {
    filename = "${path.module}/../processing_handler.zip"
    function_name = "${var.process_lambda_name}"
    role = aws_iam_role.process_role.arn
    runtime = "python3.11"
    handler = "processing_handler.processing_handler"
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
}