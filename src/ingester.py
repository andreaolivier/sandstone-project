from datetime import datetime as dt
import json
import os
from pg8000.native import Connection
from dotenv import load_dotenv
import boto3
from src.utils.ingestion import get_all_table_data


def get_connection():
    """Establishes a connection to a database and returns the connection
    object.
        Returns:
            column_names (list): All column names from table_name.
    """
    return Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )


def get_object_list(s3, bucket_name):
    """Returns all the objects in a bucket from the passed bucket_name.
        Parameters:
            s3 (botocore.client.S3): An S3 client.
            bucket_name (str): The name of the S3 bucket.
        Returns:
            bucket_object_list (list): A list of bucket objects.
    """
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        file_names = [bucket_obj['Key']
                      for bucket_obj in response['Contents']]

        return file_names
    return []


def get_last_ids(s3, bucket_name):
    """Returns the last_ids dictionary from an existing S3 Object
        Parameters:
            s3 (botocore.client.S3): An S3 client.
            bucket_name (str): The name of the S3 bucket.
        Returns:
            last_ids (dict): The primary key id number for each table from the
            previous ingestion.
    """
    bucket_objects = get_object_list(s3, bucket_name)

    if len(bucket_objects) == 0:
        return {}

    latest_file = sorted(bucket_objects)[-1]

    s3_response = s3.get_object(
        Bucket=bucket_name,
        Key=latest_file
    )

    file_content = s3_response.get('Body').read()
    json_content = json.loads(file_content)

    return json_content['last_ids']


def check_for_new_values(data):
    """Returns a boolean if the table data passed contains any new values in
    the table data meaning there is data to upload.
            data (dict): The big table data dictionary.
        Returns:
            new_values (bool): If there are values in the dictionary.
    """
    for index, data_values in enumerate(list(data.values())):
        if index == 0:
            continue
        for value in data_values.values():
            if value != []:
                return True
    return False


def ingestion_handler():
    """Handles the ingestion process. Checks for existing S3 Object if there
    isn't one downloads everything from the database and saves it in a file
    in the format of 'year-month-day/hour-minute.json'. If there is an existing
    file it extracts the last_id and only uploads the object if there are new
    changes from the database.
    """
    try:
        s3 = boto3.client('s3')
        conn = get_connection()

        bucket_name = 'tester-bucket-sandstone'

        last_ids = get_last_ids(s3, bucket_name)

        data = get_all_table_data(conn, last_ids)

        if check_for_new_values(data):
            json_str = json.dumps(data, default=str)

            date = dt.today().strftime('%y-%m-%d')
            hour = dt.today().strftime('%H-%M')
            
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{date}/{hour}.json",
                Body=json_str,
            )
    except s3.exceptions.NoSuchKey as NoKeyError:
        print(NoKeyError)
    except Exception as e:
        print(e)


load_dotenv()
ingestion_handler()
