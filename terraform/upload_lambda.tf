resource "aws_lambda_function" "upload_lambda" {
    filename = "${path.module}/../upload.zip"
    function_name = "${var.upload_lambda}"
    role = aws_iam_role.upload_role.arn
    # create upload role
    runtime = "python3.11"
    handler = "upload.lambda_handler"
    layers = ["arn:aws:lambda:eu-west-2:572843110802:layer:updated_layer:1", 
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:3"]
    timeout = 60
    environment {
      variables = {
      DW_USER = var.dw_user,
      DW_NAME = var.dw_name,
      DW_PORT = var.dw_port,
      DW_HOST = var.dw_host,
      DW_PASSWORD = var.dw_password
    }
    }
    depends_on = [ aws_cloudwatch_log_group.upload_lambda ]
}