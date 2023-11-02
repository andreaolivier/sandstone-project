provider "aws" {
  region     = "eu-west-2"
  access_key = secrets.ACCESS_KEY
  secret_key = secrets.SECRET_KEY
}