resource "aws_scheduler_schedule" "ingester_schedule" {
    description = "This scheduler should trigger the ingester lambda function every 10 minutes."
    name = "${var.ingester_scheduler_name}"
    schedule_expression = "rate(10 minutes)"
    target {
      arn = aws_lambda_function.ingester_lambda.arn
      role_arn = aws_iam_role.scheduler_role.arn
    }
    flexible_time_window {
      mode = "OFF"
    }
}