resource "aws_s3_bucket" "ingested_data_bucket" {
  bucket = "sandstone-ingested-data-testtest"
}

resource "aws_s3_bucket" "dependencies_bucket" {
  bucket = "sandstone-dependencies-testtest"
}

resource "aws_s3_bucket" "processed_data_bucket" {
  bucket = "sandstone-processed-data-testtest"
}