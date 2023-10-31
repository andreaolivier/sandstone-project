from pprint import pprint
import boto3

def get_column_names(conn, table_name):
    data = conn.run("SELECT column_name FROM information_schema.columns where table_name = '%s';" % table_name)
    return [column_name[0] for column_name in data]

def get_table_names(conn):
    data = conn.run("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' and table_type = 'BASE TABLE'")
    return [table_name[0] for table_name in data if table_name[0] != '_prisma_migrations']

def get_data(conn, table_name, query_param=''):
    column_names = get_column_names(conn, table_name)
    query = 'SELECT * from %s '
    query += query_param
    query += ';'
    data = conn.run(query % table_name)

    table = {}

    for row in data:
        for index, element in enumerate(row):
            if column_names[index] not in table:
                table[column_names[index]] = []

            table[column_names[index]].append(element)

    return table


def upload_file_to_s3_bucket_first_time():
    client = boto3.client('s3')
    client.upload_file('alltables.json', 'nc-de-pb', 'alltables.json')

'''one function: if s3 bucket empty, take snapshop of all tables. if s3 bucket is not empty, look at the most recent file and look at last sales_order_id and get everything after'''