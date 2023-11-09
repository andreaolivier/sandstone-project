resource "aws_lambda_function" "upload_lambda" {
    filename = "${path.module}/../upload.zip"
    function_name = "${var.upload_lambda}"
    role = aws_iam_role.upload_role.arn
    # create upload role
    runtime = "python3.11"
    handler = "upload.lambda_handler"
    # layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
    # environment {
    #   variables = {
    #     DB_USER = secrets.DW_USER,
    #     DB_NAME = secrets.DW_NAME,
    #     DB_PORT = secrets.DW_PORT,
    #     DB_HOST = secrets.DW_HOST,
    #     DB_PASSWORD = secrets.DW_PASSWORD
    #   }
    # }
}