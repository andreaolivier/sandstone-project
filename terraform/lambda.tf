resource "aws_iam_role" "ingester_role" {
    name = "ingester_role"
    assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${var.python_file_name}.py"
    output_path = "${var.lambda_name}_payload.zip"
}

resource "aws_lambda_function" "ingester_lambda" {
    filename = "${var.lambda_name}_payload.zip"
    function_name = "${var.lambda_name}"
    role = aws_iam_role.ingester_role.arn
    runtime = "python3.11"
    handler = "${var.python_file_name}.ingestion_handler"
}