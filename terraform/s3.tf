resource "aws_s3_bucket" "data_bucket" {
  bucket = "sandstone-ingest"
}

resource "aws_s3_bucket" "code_bucket" {
  bucket = "sandstone-dependencies"
}