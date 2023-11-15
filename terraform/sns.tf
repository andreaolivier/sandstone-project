resource "aws_sns_topic" "alarm_logging_sns" {
    #This simply creates the SNS topic, which presently does nothing.
	name = "logging-sns-topic"
	}



resource "aws_sns_topic_subscription" "alarm_subscription" {
    #This creates our group email's subscription to the SNS topic. This will send an email that will activate the subscription once we respond.
	protocol = "email"
    topic_arn = "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:logging-sns-topic"
	endpoint = "sandstone.de@gmail.com"

    depends_on = [ aws_sns_topic.alarm_logging_sns ]
	}

#This topic will need to be connected to an alarm in the aws_cloudwatch_metric_alarm resource, by putting its arn into the Alarm Actions parameter.

# resource "aws_sns_topic" "process_logging_sns" {
#     #This simply creates the SNS topic, which presently does nothing.
# 	name = "process-logging-sns-topic"
# 	}



# resource "aws_sns_topic_subscription" "process_subscription" {
#     #This creates our group email's subscription to the SNS topic. This will send an email that will activate the subscription once we respond.
# 	protocol = "email"
#     topic_arn = "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:process-logging-sns-topic"
# 	endpoint = "sandstone.de@gmail.com"

#     depends_on = [ aws_sns_topic.process_logging_sns ]
# 	}

# resource "aws_sns_topic" "upload_logging_sns" {
#     #This simply creates the SNS topic, which presently does nothing.
# 	name = "upload-logging-sns-topic"
# 	}

# resource "aws_sns_topic_subscription" "upload_subscription" {
#     #This creates our group email's subscription to the SNS topic. This will send an email that will activate the subscription once we respond.
# 	protocol = "email"
#     topic_arn = "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:upload-logging-sns-topic"
# 	endpoint = "sandstone.de@gmail.com"

#     depends_on = [ aws_sns_topic.upload_logging_sns ]
# 	}

# #This topic will need to be connected to an alarm in the aws_cloudwatch_metric_alarm resource, by putting its arn into the Alarm Actions parameter.