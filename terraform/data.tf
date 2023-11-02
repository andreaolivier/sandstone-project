data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester.py"
    output_path = "${path.module}/../${var.lambda_name}.zip"
}

data "archive_file" "util-ingestion" {
    type = "zip"
    source_dir = "${path.module}/../src/python"
    output_path = "${path.module}/../python.zip"
}

data "aws_iam_policy_document" "scheduler_document" {
  statement {
    actions = ["lambda:InvokeFunction"]

    resources = ["${aws_lambda_function.ingester_lambda.arn}"]
  }
}
