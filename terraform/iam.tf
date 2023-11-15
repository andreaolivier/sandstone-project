# Ingester IAM
# Creates role for Lambda

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

# Creates data for por Cloudwatch policy

data "aws_iam_policy_document" "cw_document" {
  # statement {

  #   actions = ["logs:CreateLogGroup"]

  #   resources = [
  #     "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
  #   ]
  # }

  statement {

    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}:*"
    ]
  }
}

# Creates Cloudwatch policy

resource "aws_iam_policy" "cw_policy" {
  name = "cw-policy-${var.lambda_name}"
  policy      = data.aws_iam_policy_document.cw_document.json
}

# Attaches Cloudwatch policy to Lambda role

resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.ingester_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

# Creates data for por S3 policy allowing ingestion lambda to post object to S3

data "aws_iam_policy_document" "s3_document" {
  statement {
    actions = ["s3:PutObject",
              "s3:GetObject",
              "s3:ListBucket"]
    resources = [
      "${aws_s3_bucket.ingested_data_bucket.arn}",
      "${aws_s3_bucket.ingested_data_bucket.arn}/*"
    ]
  }
}

# Creates S3 policy

resource "aws_iam_policy" "s3_policy" {
  name = "s3-policy-${var.lambda_name}"
  policy      = data.aws_iam_policy_document.s3_document.json
}

# Attaches S3 policy to Lambda role

resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  role       = aws_iam_role.ingester_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

# Creates role for scheduler

resource "aws_iam_role" "scheduler_role" {
    name = "scheduler_role"
    assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["sts:AssumeRole"],
        Effect = "Allow",
        Principal = {
          Service = ["scheduler.amazonaws.com"]
        }
      }
    ]
  })
}

# Creates Scheduler policy

resource "aws_iam_policy" "scheduler_policy" {
  name_prefix = "scheduler-policy-${var.ingester_scheduler_name}"
  policy = data.aws_iam_policy_document.scheduler_document.json 
}

# Attaches Scheduler policy to Scheduler role

resource "aws_iam_role_policy_attachment" "scheduler_scheduler_policy_attachment" {
  role = aws_iam_role.scheduler_role.name
  policy_arn = aws_iam_policy.scheduler_policy.arn  
}

# Process IAM

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
  statement {

    actions = ["logs:CreateLogGroup"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

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

# Upload IAM

# Creates role for Lambda

resource "aws_iam_role" "upload_role" {
    name = "upload_role"
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

data "aws_iam_policy_document" "upload_cw_document" {
  statement {

    actions = ["logs:CreateLogGroup"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {

    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.upload_lambda}:*"
    ]
  }
}

# Creates Cloudwatch policy

resource "aws_iam_policy" "upload_cw_policy" {
  name = "cw-policy-${var.upload_lambda}"
  policy      = data.aws_iam_policy_document.upload_cw_document.json
}

# Attaches Cloudwatch policy to Lambda role

resource "aws_iam_role_policy_attachment" "upload_lambda_cw_policy_attachment" {
  role       = aws_iam_role.upload_role.name
  policy_arn = aws_iam_policy.upload_cw_policy.arn
}

# Creates data for por S3 policy allowing ingestion lambda to post object to S3

data "aws_iam_policy_document" "upload_s3_document" {
  statement {
    actions = [
              "s3:GetObject",
              "s3:ListBucket"]
    resources = [
      "${aws_s3_bucket.processed_data_bucket.arn}",
      "${aws_s3_bucket.processed_data_bucket.arn}/*"
    ]
  }
}

# Creates S3 policy

resource "aws_iam_policy" "upload_s3_policy" {
  name = "s3-policy-${var.upload_lambda}"
  policy      = data.aws_iam_policy_document.upload_s3_document.json
}

# Attaches S3 policy to Lambda role

resource "aws_iam_role_policy_attachment" "upload_lambda_s3_policy_attachment" {
  role       = aws_iam_role.upload_role.name
  policy_arn = aws_iam_policy.upload_s3_policy.arn
}