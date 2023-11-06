terraform {
  backend "s3" {
    bucket = "sandstone-terraform-state"
    key    = "terraform-state"
    region = "eu-west-2"
  }
}

data "aws_iam_policy_document" "s3_terraform_document" {
  statement {
    actions = ["s3:PutObject",
              "s3:GetObject",
              "s3:ListBucket"]
    resources = [
      "${aws_s3_bucket.terraform_state_bucket.arn}",
      "${aws_s3_bucket.terraform_state_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "s3_terraform_policy" {
  name = "s3-terraform-policy"
  policy      = data.aws_iam_policy_document.s3_terraform_document.json
}


# resource "aws_iam_role" "terraform_s3_role" {
#   name = "terraform_s3_role"

#   assume_role_policy = jsonencode({
#     Version: "2012-10-17",
#     Statement: [
#       {
#         Effect: "Allow",
#         Principal: {
#           Service: "s3.amazonaws.com"
#         },
#         Action: "sts:AssumeRole"
#       }
#     ]
#   })
# }

resource "aws_iam_role_policy_attachment" "terraform_s3_role_attachment" {
  role       = aws_iam_role.terraform_s3_role.name
  policy_arn = aws_iam_policy.s3_terraform_policy.arn
}