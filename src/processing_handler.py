import boto3
import json
import logging
from botocore.exceptions import ClientError
from processing import get_currency_data, dim_counter_party, dim_date, make_new_design_table, to_dim_location, create_dim_staff, fact_sales_util, parquet_converter


logger = logging.getLogger('TransformLogger')
logger.setLevel(logging.INFO)


def processing_handler(event, context):
    '''
    This finds the latest file in the s3 bucket, gets it from the bucket, and
    runs transformation functions on it.
    '''
    try:
        utils_dict = {
            'currency': get_currency_data,
            'counterparty': dim_counter_party,
            'date': dim_date,
            'design': make_new_design_table,
            'location': to_dim_location,
            'staff': create_dim_staff,
            'sales_order': fact_sales_util,
        }
        json_data = get_latest_file(event)
        processed_data = []
        processed_table_names = []
        for key, value in json_data.items():
            for data in value:
                if data == []:
                    continue
                else:
                    processed_data.append(utils_dict[key](json_data))
                    processed_table_names.append(key)

        parquet_converter(processed_data, processed_table_names)

        event_names_for_erros = get_object_path(event)
        s3_object_name = event_names_for_erros['object']

    except KeyError:
        logger.error(
            'There was an issue with the bucket data, please investigate.')
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'No object found - {s3_object_name}')
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error('Processed data bucket is missing')
        else:
            raise
    except InvalidFileTypeError:
        logger.error(f'File {s3_object_name} is not a JSON')
    except Exception as e:
        logger.error(e)
        raise RuntimeError


def get_latest_file(event):
    '''This is run within the handler to retrieve the object that triggered
    the most recent event.
    '''
    try:
        event_names = get_object_path(event)
        s3_bucket_name = event_names['bucket']
        s3_object_name = event_names['object']
        logger.info(f'Bucket is {s3_bucket_name}')
        logger.info(f'Object is {s3_object_name}')

        if s3_object_name[-4:] != 'json':
            raise InvalidFileTypeError
        s3 = boto3.client('s3')

        get_data = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_name)
        json_data = json.load(get_data['Body'])
        return json_data
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'No object found - {s3_object_name}')
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error(f'No such bucket - {s3_bucket_name}')
        else:
            raise
    except InvalidFileTypeError:
        logger.error(f'File {s3_object_name} is not a JSON')
    except Exception as e:
        logger.error(e)
        raise RuntimeError


def get_object_path(event_file):
    """Extracts bucket and object references from Records field of event."""
    return {'bucket': event_file['Records'][0]['s3']['bucket']['name'],
            'object': event_file['Records'][0]['s3']['object']['key']}


class InvalidFileTypeError(Exception):
    '''Handles errors where file is not a json'''
