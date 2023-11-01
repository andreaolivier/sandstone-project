data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester.py"
    output_path = "${path.module}/../${var.lambda_name}.zip"
}
