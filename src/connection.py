from pg8000.native import Connection
import os


def get_connection():
    return Connection(
        user='project_user_7',
        database='totesys',
        port=os.environ.get('DB_PORT'),
        host=os.environ.get('DB_HOST'),
        password=os.environ.get('DB_PASSWORD')
    )

