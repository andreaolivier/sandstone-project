"""This module contains the ingestion functions used to collect all the data
from the PSQL database.
"""
from pg8000.native import identifier, literal
import json

def get_column_names(conn, table_name):
    """Returns the names of all the columns in the passed table from the
    connected PSQL database.
        Parameters:
            conn (pg8000.native.connection): A database connection.
            table_name (str): PSQL table name.
        Returns:
            column_names (list): All column names from table_name.
    """
    data = conn.run(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    where table_name = {literal(table_name)};
                    """)

    return [column_name[0] for column_name in data]


def get_table_names(conn):
    """Returns the names of all the tables from the connected PSQL database.
        Parameters:
            conn (pg8000.native.connection): A database connection.
        Returns:
            column_names (list): All column names the connected database except
            '_prisma_migrations' table.
    """
    data = conn.run("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                        and table_type = 'BASE TABLE'
                    """)

    return [table_name[0] for table_name in data
            if table_name[0] != '_prisma_migrations']


def get_table_data(conn, table_name, last_id=0):
    """Returns all the rows whose primary key id is higher than the last_id
    from the passed PSQL table.
        Parameters:
            conn (pg8000.native.connection): A database connection.
            table_name (str): PSQL table name.
            last_id (int): The last primary key id number from the
            previous ingestion, if no previous ingestion, defaults to 0.
        Returns:
            tables (dict): Returns all the data in the table_name from the
            connected PSQL database.
    """
    columns = get_column_names(conn, table_name)

    data = conn.run(f"""
                    SELECT * from {identifier(table_name)}
                    where {identifier(columns[0])} > {literal(last_id)}
                    order by {identifier(columns[0])} asc;
                    """)
    table = {}

    for column in columns:
        table[column] = []

    for row in data:
        for index, element in enumerate(row):
            table[columns[index]].append(element)

    return table


def get_all_table_data(conn, last_ids={}):
    """Returns the all the table data from get_data() in a dictionary and
    creates a key of all the last_ids.
        Parameters:
            conn (pg8000.native.connection): A database connection.
            last_ids (dict): A dictionary containing all the last primary key
            id numbers from the previous ingestion, if no previous ingestion,
            all values default to 0.
        Returns:
            big_dict (dict): Returns all the data for all the tables.
    """
    big_dict = {}
    big_dict['last_ids'] = {}
    table_names = get_table_names(conn)

    for table in table_names:
        primary_key = get_column_names(conn, table)[0]

        if table not in last_ids:
            last_ids[table] = 0

        big_dict[table] = get_table_data(conn, table, last_ids[table])

        if big_dict[table][primary_key] != []:
            big_dict['last_ids'][table] = big_dict[table][primary_key][-1]
        else:
            big_dict['last_ids'][table] = last_ids[table]

    return big_dict


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
