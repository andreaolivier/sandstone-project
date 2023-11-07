resource "aws_lambda_layer_version" "lambda_layer" {
    filename   = "${path.module}/../python1.zip"
    layer_name = "pandas_module_layer"
    compatible_runtimes = ["python3.11"]
}