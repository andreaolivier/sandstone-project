resource "aws_cloudwatch_log_metric_filter" "ingester_error_filtering" {
	name = "IngesterErrorFiltering"
	pattern = "Error"
	log_group_name = "log-group:/aws/lambda/LAMBDANAMEHERE"
	
	metric_transformation {
		name = "ErrorCount"
		namespace = "IngesterLogging"
		value = "1"
		}
	}

resource "aws_cloudwatch_metric_alarm" "ingester_alarm" {
    alarm_name = "CloudwatchAlarm"
    namespace = "IngesterLogging"
    metric_name = "ErrorCount"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    threshold = 1
    statistic = "SampleCount"
    period = 300
    alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:IngesterLoggingSnsTopic"]
}

resource "aws_cloudwatch_metric_alarm" "duration_error" {
    alarm_name = "DurationAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    namespace = "AWS/Lambda"
    threshold = 1200
    metric_name = "Duration"
    statistic = "Maximum"
    period = 60
    alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:IngesterLoggingSnsTopic"]
}