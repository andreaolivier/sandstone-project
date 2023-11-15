import boto3
import json
import logging
from botocore.exceptions import ClientError
from processing import to_dim_date, to_dim_currency, to_dim_counter_party, \
    to_dim_design, to_dim_location, to_dim_staff, \
    to_fact_sales, parquet_converter


logger = logging.getLogger('TransformLogger')
logger.setLevel(logging.INFO)


def processing_handler(event, context):
    '''
    This finds the latest file in the s3 bucket, gets it from the bucket, and
    runs transformation functions on it.
    '''
    try:
        processed_data = []
        processed_table_names = []

        s3 = boto3.client('s3')
        all_objects = s3.list_objects_v2(
            Bucket='sandstone-processed-data'
        )

        if 'Contents' not in all_objects:

            date = to_dim_date()
            processed_data.append(date)
            processed_table_names.append('dim_date')

        utils_dict = {
            'currency': to_dim_currency,
            'counterparty': to_dim_counter_party,
            'design': to_dim_design,
            'address': to_dim_location,
            'staff': to_dim_staff,
            'sales_order': to_fact_sales,
        }

        lookup = {
            'currency': 'dim_currency',
            'counterparty': 'dim_counterparty',
            'design': 'dim_design',
            'address': 'dim_location',
            'staff': 'dim_staff',
            'sales_order': 'fact_sales_order'
        }

        json_data = get_latest_file(event, s3)

        for key, value in json_data.items():
            contains_data = False
            for data in value:
                if value[data] == []:
                    contains_data = False
                elif key in utils_dict.keys():
                    contains_data = True
            if contains_data:
                processed_data.append(utils_dict[key](json_data))
                processed_table_names.append(lookup[key])

        parquet_converter(processed_data, processed_table_names, s3)
    except KeyError as e:
        logger.error(event['Records'][0]['s3']['object']['key'])
        logger.error(e)
        logger.error(
            'There was an issue with the bucket data, please investigate.')
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(c)
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error('Processed data bucket is missing')
        else:
            raise
    except InvalidFileTypeError:
        logger.error('File is not a JSON')
    except Exception as e:
        logger.error(e)


def get_latest_file(event, s3):
    '''This is run within the handler to retrieve the object that triggered
    the most recent event.
    '''
    logger.info('GET_LATEST_FILE')

    event_names = get_object_path(event)
    s3_bucket_name = event_names['bucket']
    s3_object_name = event_names['object']

    logger.info(f'Bucket is {s3_bucket_name}')
    logger.info(f'Object is {s3_object_name}')

    if s3_object_name[-4:] != 'json':
        raise InvalidFileTypeError

    get_data = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_name)
    json_data = json.load(get_data['Body'])
    return json_data


def get_object_path(event_file):
    logger.info('GET_OBJECT_PATH')
    """Extracts bucket and object references from Records field of event."""
    return {'bucket': event_file['Records'][0]['s3']['bucket']['name'],
            'object': event_file['Records'][0]['s3']['object']['key']}


class InvalidFileTypeError(Exception):
    '''Handles errors where file is not a json'''
