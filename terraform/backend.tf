terraform {
  backend "s3" {
    bucket = "sandstone-terraform"
    key    = "terraform-state"
    region = "eu-west-2"
  }
}