variable "amazon_account_id" {}

resource "aws_sns_topic" "ingester_logging_sns" {
    #This simply creates the SNS topic, which presently does nothing.
	name = "IngesterLoggingSnsTopic"
	}



resource "aws_sns_topic_subscription" "ingester_subscription" {
    #This creates our group email's subscription to the SNS topic. This will send an email that will activate the subscription once we respond.
	protocol = "email"
    topic_arn = "arn:aws:sns:eu-west-2:${var.amazon_account_id}:ingester_logging_sns_topic"
	endpoint = "sandstone.de@gmail.com"
	}




#This topic will need to be connected to an alarm in the aws_cloudwatch_metric_alarm resource, by putting its arn into the Alarm Actions parameter.