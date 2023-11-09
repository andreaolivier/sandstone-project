import pg8000
import pandas as pd
import awswrangler as wr
import pg8000.dbapi
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        conn = pg8000.dbapi.connect(
            user=os.environ['DB_USER'],
            database=os.environ['DB_NAME'],
            port=os.environ['DB_PORT'],
            host=os.environ['DB_HOST'],
            password=os.environ['DB_PASSWORD']
        )
        cursor = conn.cursor()

        s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_object_name = event['Records'][0]['s3']['object']['key']

        logger.info('Bucket is %s', s3_bucket_name)
        logger.info('Object key is %s', s3_object_name)

        if s3_object_name[-7] != 'parquet':
            raise InvalidFileTypeError

        df = wr.s3.read_parquet(
            path=[f's3://{s3_bucket_name}/{s3_object_name}'])

        table_dict = df.to_dict('tight')

        table_name = s3_object_name[15:-8]

        placeholders = ', '.join(['%s'] * len(table_dict['data'][0]))

        for row in table_dict['data']:
            cursor.execute(
                f"INSERT INTO {table_name} "
                f" VALUES ({placeholders}) ",
                tuple(f'{str(i)}' for i in row)
            )

        conn.commit()
        logger.info('upload success')
    except KeyError as k:
        logger.error('Error retrieving data %s', k)
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'No object found - {s3_object_name}')
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error(f'No such bucket - {s3_bucket_name}')
        else:
            raise
    except UnicodeError:
        logger.error(f'File {s3_object_name} is not a valid text file')
    except InvalidFileTypeError:
        logger.error(f'File {s3_object_name} is not a valid text file')
    except Exception as e:
        logger.error(e)
        raise RuntimeError


class InvalidFileTypeError(Exception):
    """Traps error where file type is not txt."""
    pass
