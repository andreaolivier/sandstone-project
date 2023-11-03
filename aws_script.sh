#!/usr/local/bin/bash

aws s3 ls | awk '{print $3}'

for i in s3://sandstone-ingested-data-testtest; do
  aws s3 rm $i --recursive --include "*"
  aws s3 rb $i;
done

for i in s3://sandstone-processed-data-testtest; do
  aws s3 rm $i --recursive --include "*"
  aws s3 rb $i;
done
