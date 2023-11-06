import boto3
import json
from botocore.exceptions import ClientError


def get_latest_file():
    '''
    This finds the latest file, and returns its contents as a dictionary of dictonaries.
    '''
    try:
        s3 = boto3.client('s3')
        bucket_name = 'sandstone-ingested-data'
        response = s3.list_objects_v2(Bucket=bucket_name)['Contents']
        last_modified = lambda response: int(response['LastModified'].strftime('%s'))
        latest_file = [response['Key'] for response in sorted(response, key=last_modified, reverse=True)][0]
        get_data = s3.get_object(Bucket=bucket_name, Key=latest_file)
        json_data = json.load(get_data['Body'])
        return json_data
    except KeyError:
        print('There was an issue with the bucket data, please investigate.')
    except ClientError:
        print('There was an issue connecting to AWS')


def get_table_from_dict(latest_data, choice):
    '''This takes two arguments, representing the return from get_latest_file and the chosen table name respectively, and extracts the data for the table matching choice. It returns table data.'''
    try:
        return latest_data[choice]
    except KeyError:
        print('You entered an invalid table name')
