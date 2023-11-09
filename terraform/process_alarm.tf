resource "aws_cloudwatch_metric_alarm" "process_alarm" {
#This triggers an alarm when the process function reports an error.
    alarm_name = "CloudwatchAlarm"
    namespace = "ProcessLogging"
    metric_name = "ErrorCount"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    threshold = 1
    statistic = "SampleCount"
    period = 300
    alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:process-logging-sns-topic"]
}

resource "aws_cloudwatch_log_metric_filter" "process_error_filtering" {
#This adds a filter for errors in the logs sent to the log group.
#The log group should be automatically created by the lambda function, so this will need to be amended once that's done.
#The task says that this should be saved for major errors, so this should probably be rewritten when we add logging and error reporting to the ingester.
	name = "ProcessErrorFiltering"
	pattern = "Error"
	log_group_name = "/aws/lambda/${var.process_lambda_name}"
	
	metric_transformation {
		name = "ErrorCount"
		namespace = "ProcessLogging"
		value = "1"
		}
    depends_on = [ aws_lambda_function.process_lambda ]
	}



resource "aws_cloudwatch_metric_alarm" "process_duration_alarm" {
#I thought it might be a good idea to add a duration error similar to the one from the sprint.
#If I understand this right it should raise an error when the process runs for more than 10 minutes.
#This shouldn't need a filter since it uses the AWS/Lambda namespace, which lambda functions automatically send metrics to.
    alarm_name = "ProcessDurationAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    namespace = "AWS/Lambda"
    threshold = 60000
    metric_name = "Duration"
    statistic = "Maximum"
    period = 120
    alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:process-logging-sns-topic"]
}