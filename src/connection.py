from pg8000.native import Connection
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

client = botocore.session.get_session().create_client('secretsmanager')
cache_config = SecretCacheConfig()
cache = SecretCache( config = cache_config, client = client)

USER = cache.get_secret_string('DB_USER')
NAME = cache.get_secret_string('DB_NAME')
PORT = cache.get_secret_string('DB_PORT')
HOST = cache.get_secret_string('DB_HOST')
PASSWORD = cache.get_secret_string('DB_PASSWORD')


def get_connection():
    '''Connects to the totesys database using
    credentials stored in aws secrets'''
    return Connection(
        user=USER,
        database=NAME,
        port=PORT,
        host=HOST,
        password=PASSWORD
    )

