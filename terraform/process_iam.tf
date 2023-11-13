# Creates role for Lambda

resource "aws_iam_role" "process_role" {
    name = "process_role"
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

# Creates data for por Cloudwatch policy

data "aws_iam_policy_document" "process_cw_document" {
  # statement {

  #   actions = ["logs:CreateLogGroup"]

  #   resources = [
  #     "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
  #   ]
  # }

  statement {

    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.process_lambda_name}:*"
    ]
  }
}

# Creates Cloudwatch policy

resource "aws_iam_policy" "process_cw_policy" {
  name = "cw-policy-${var.process_lambda_name}"
  policy      = data.aws_iam_policy_document.process_cw_document.json
}

# Attaches Cloudwatch policy to Lambda role

resource "aws_iam_role_policy_attachment" "process_lambda_cw_policy_attachment" {
  role       = aws_iam_role.process_role.name
  policy_arn = aws_iam_policy.process_cw_policy.arn
}

# Creates data for por S3 policy allowing ingestion lambda to post object to S3

data "aws_iam_policy_document" "process_s3_document" {
  statement {
    actions = ["s3:PutObject",
              "s3:GetObject",
              "s3:ListBucket",
              "s3:ListObjects"]
    resources = [
      "${aws_s3_bucket.processed_data_bucket.arn}",
      "${aws_s3_bucket.ingested_data_bucket.arn}",
      "${aws_s3_bucket.ingested_data_bucket.arn}/*",
      "${aws_s3_bucket.processed_data_bucket.arn}/*"
    ]
  }
}

# Creates S3 policy

resource "aws_iam_policy" "process_s3_policy" {
  name = "s3-policy-${var.process_lambda_name}"
  policy      = data.aws_iam_policy_document.process_s3_document.json
}

# Attaches S3 policy to Lambda role

resource "aws_iam_role_policy_attachment" "process_lambda_s3_policy_attachment" {
  role       = aws_iam_role.process_role.name
  policy_arn = aws_iam_policy.process_s3_policy.arn
}

# # Creates role for scheduler

# resource "aws_iam_role" "process_scheduler_role" {
#     name = "process_scheduler_role"
#     assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = ["sts:AssumeRole"],
#         Effect = "Allow",
#         Principal = {
#           Service = ["scheduler.amazonaws.com"]
#         }
#       }
#     ]
#   })
# }

# # Creates Scheduler policy

# resource "aws_iam_policy" "process_scheduler_policy" {
#   name_prefix = "scheduler-policy-${var.process_scheduler_name}"
#   policy = data.aws_iam_policy_document.process_scheduler_document.json 
# }

# # Attaches Scheduler policy to Scheduler role

# resource "aws_iam_role_policy_attachment" "process_scheduler_scheduler_policy_attachment" {
#   role = aws_iam_role.process_scheduler_role.name
#   policy_arn = aws_iam_policy.process_scheduler_policy.arn  
# }

