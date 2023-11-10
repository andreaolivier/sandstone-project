import boto3
import json
import logging
from botocore.exceptions import ClientError
from processing import get_currency_data, dim_counter_party, to_dim_date, \
    make_new_design_table, to_dim_location, create_dim_staff, \
        fact_sales_util, parquet_converter


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
        
        if all_objects['Contents']:
            pass
        else:
            date = to_dim_date()
            processed_data.append(date)
            processed_table_names.append('dim_date')

        utils_dict = {
            'currency': get_currency_data,
            'counterparty': dim_counter_party,
            'design': make_new_design_table,
            'address': to_dim_location,
            'staff': create_dim_staff,
            'sales_order': fact_sales_util,
        }

        lookup = {
            'currency': 'dim_currency',
            'counterparty': 'dim_counterparty',
            'design': 'dim_design',
            'address': 'dim_location',
            'staff': 'dim_staff',
            'sales_order': 'fact_sales_order'
        }

        json_data = get_latest_file(event)
        
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

        parquet_converter(processed_data, processed_table_names)

        s3_object_name = get_object_path(event)['object']

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
