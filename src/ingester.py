from datetime import datetime as dt
import json
import os
import logging
from pg8000.native import Connection
from dotenv import load_dotenv
import boto3
from src.utils.ingestion import get_all_table_data, get_last_ids, check_for_new_values

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

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
    # except InterfaceError as pg_err:
    #     print(pg_err)
    #     logger.info(f'Critical pg8000 error: {pg_err}')
    # except s3.exceptions.NoSuchKey as NoKeyError:
    #     print(NoKeyError)
    except Exception as e:
        print(e, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,")


load_dotenv()
ingestion_handler()
