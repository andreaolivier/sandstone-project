resource "aws_lambda_layer_version" "automated_layer" {
  layer_name = "sandstone-automated-layer"
  filename = "${path.module}/../custom_layer.zip"
}