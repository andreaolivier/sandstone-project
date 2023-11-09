data "archive_file" "upload_lambda" {
    type = "zip"
    source_file = "${path.module}/../src/upload.py"
    output_path = "${path.module}/../upload.zip"
}