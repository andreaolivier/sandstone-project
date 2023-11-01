from pg8000.native import Connection
from utils.ingestion import get_table_names, get_data
import json
import boto3
from pprint import pprint


def get_connection():
   return Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )

conn = get_connection()

def get_all_tables():
    big_dict = {}
    table_names = get_table_names(conn)
    for table in table_names:
        big_dict[table] = get_data(conn, table)
    with open('alltables.json', 'w') as file:
        file.write(json.dumps(big_dict, default=str))

print(get_all_tables())


def upload_data_to_s3():
    client = boto3.client('s3')
    client.upload_file('alltables.json', 'nc-de-pb', 'alltables.json')
