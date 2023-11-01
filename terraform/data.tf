data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester.py"
    output_path = "${path.module}/../${var.lambda_name}_payload.zip"
}

data "aws_iam_policy_document" "cw_document" {
  statement {

    actions = ["logs:CreateLogGroup"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {

    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}:*"
    ]
  }
}

data "aws_iam_policy_document" "scheduler_document" {
  statement {
    actions = ["lambda:InvokeFunction"]

    resources = ["${aws_lambda_function.ingester_lambda.arn}"]
  }
}