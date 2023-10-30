provider "aws" {
  region     = "eu-west-2"
  access_key = secrets.access_key
  secret_key = secrets.secret_key
}