terraform {
  backend "s3" {
    bucket = "sandstone-terraform-state"
    key    = "terraform-state"
    region = "eu-west-2"
  }
}