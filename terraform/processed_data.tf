data "archive_file" "process_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/processing_handler.py"
    output_path = "${path.module}/../processing_handler.zip"
}

data "archive_file" "processing_python_layer_zip" {
    type = "zip"
    source_dir = "${path.module}/../python"
    output_path = "${path.module}/../python.zip"
}

# data "aws_iam_policy_document" "scheduler_document" {
#   statement {
#     actions = ["lambda:InvokeFunction"]

#     resources = ["${aws_lambda_function.process_lambda.arn}"]
#   }
# }