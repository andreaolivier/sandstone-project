resource "aws_lambda_function" "ingester_lambda" {
    filename = "${path.module}/../${var.lambda_name}.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "${var.python_file_name}.ingestion_handler"
}