data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester.py"
    output_path = "${path.module}/../python1.zip"
}

data "aws_iam_policy_document" "scheduler_document" {
  statement {
    actions = ["lambda:InvokeFunction"]

    resources = ["${aws_lambda_function.ingester_lambda.arn}"]
  }
}
