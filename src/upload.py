import pg8000
import pandas as pd
import awswrangler as wr
from pg8000.native import Connection, identifier, literal


def get_connection():
    """Establishes a connection to a database and returns the connection
    object.
        Returns:
            column_names (list): All column names from table_name.
    """
    return Connection(
        user='andrea',
        database='test_processing',
        port=5432,
        host='localhost',
        password='password123'
    )


def upload_handler():
    # s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    # s3_object_name = event['Records'][0]['s3']['object']['key']
    s3_object_name = '23-11-01/10-12/test.parquet'

    # if s3_object_name[-7] != 'parquet':
    #     raise InvalidFileTypeError

    df = wr.s3.read_parquet(
        path=[f's3://tester-bucket-sandstone/{s3_object_name}'])
    table_dict = df.to_dict('tight')
    table_name = s3_object_name[15:-8]
    columns = [str(f'"{val}"') for val in table_dict['columns']]

    for row in table_dict['data']:
        # values = [str(f'"{val}"') for val in row if ]
        # print(f'''insert into test values ({', '.join(values)}); ''')  

        get_connection().run('insert into test (department_id, department_name, location, manager, created_at, last_updated) values (1, "Sales", "Manchester", "Richard Roma", "2022-11-03 14:20:49.962000", "2022-11-03 14:20:49.962000") ')


upload_handler()


class InvalidFileTypeError(Exception):
    """Traps error where file type is not txt."""
    pass
