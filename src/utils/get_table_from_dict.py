import boto3
import pandas
import json


def get_latest_file():
 
    s3 = boto3.client('s3')
    bucket_name = 'sandstone-ingested-data'
    response = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    last_modified = lambda response: int(response['LastModified'].strftime('%s'))
    latest_file = [response['Key'] for response in sorted(response, key=last_modified, reverse=True)][0]
    get_data = s3.get_object(Bucket=bucket_name, Key=latest_file)
    json_data = json.load(get_data['Body'])
    return json_data

def get_table_from_dict(latest_data, choice):
    return latest_data[choice]

