resource "aws_s3_bucket" "ingested_data_bucket" {
  bucket = "sandstone-ingested-data"
}

resource "aws_s3_bucket" "processed_data_bucket" {
  bucket = "sandstone-processed-data"
}

# resource "aws_s3_bucket" "terraform_state_bucket" {
#   bucket = "sandstone-terraform-state"
# }