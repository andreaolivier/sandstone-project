resource "aws_s3_bucket" "ingested_data_bucket" {
  bucket = "sandstone-ingested-data"
}

resource "aws_s3_bucket" "processed_data_bucket" {
  bucket = "sandstone-processed-data"
}

resource "aws_s3_bucket_notification" "processor_lambda_notification" {
  #This resource creates a bucket notification in the ingested data bucket.
  #This should send an event to the processer lambda, triggering it to run on the new object.
  #The s3:ObjectCreated:Put line in events should restrict it triggering to a put command, 
  #which matches the put_object command used in the ingester.py.
  #filter_suffix should restrict valid objects for the trigger to .json files.
  #All of this should require a matching permission in the process lambda.


  bucket = aws_s3_bucket.ingested_data_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.process_lambda.arn
    events = ["s3:ObjectCreated:Put"]
    filter_suffix = ".json"
    }
  depends_on = [aws_lambda_permission.allow_put_object_event]
}

resource "aws_s3_bucket_notification" "upload_lambda_notification" {
  #This should create an equivalent notification to the above for the upload lambda.


  bucket = aws_s3_bucket.processed_data_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.upload_lambda.arn
    events = ["s3:ObjectCreated:Put"]
    filter_suffix = ".parquet"
    }
  depends_on = [aws_lambda_permission.parquet_object_added]
}

resource "aws_lambda_permission" "parquet_object_added" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.upload_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.processed_data_bucket.arn
  depends_on = [ aws_cloudwatch_log_group.upload_lambda ]
}