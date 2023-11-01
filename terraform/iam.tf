resource "aws_iam_role" "ingester_role" {
    name = "ingester_role"
    assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["sts:AssumeRole"],
        Effect = "Allow",
        Principal = {
          Service = ["lambda.amazonaws.com"]
        }
      }
    ]
  })
}

resource "aws_iam_policy" "cw_policy" {
  name_prefix = "cw-policy-${var.lambda_name}"
  policy      = data.aws_iam_policy_document.cw_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.ingester_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}


