resource "aws_lambda_function" "process_lambda" {
    # filename = "${path.module}/../${var.lambda_name}.zip"
    filename = "${path.module}/../utils/processing_handler.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "processing_handler.processing_handler"
    # handler = "${var.python_file_name}.ingestion_handler"
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
}