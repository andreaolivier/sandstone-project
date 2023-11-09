terraform {
  backend "s3" {
    bucket = "sandstone-terraform-state"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}