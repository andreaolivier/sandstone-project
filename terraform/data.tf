data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "ingester_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/ingester.py"
    output_path = "${path.module}/../ingester.zip"
}

data "archive_file" "process_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/processing_handler.py"
    output_path = "${path.module}/../processing_handler.zip"
}

data "archive_file" "upload_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/upload.py"
    output_path = "${path.module}/../upload.zip"
}

data "archive_file" "layer_zip" {
    type = "zip"
    source_dir = "${path.module}/../python"
    output_path = "${path.module}/../custom_layer.zip"
    }