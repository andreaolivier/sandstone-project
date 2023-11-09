resource "aws_lambda_function" "upload_lambda" {
    filename = "${path.module}/../upload.zip"
    function_name = "${var.upload_lambda}"
    role = aws_iam_role.upload_role.arn
    # create upload role
    runtime = "python3.11"
    handler = "upload.lambda_handler"
    # layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 60
}