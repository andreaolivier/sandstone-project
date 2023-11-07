import boto3
import json
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger('TransformLogger')
#Not sure if we want to use same logger as ingestion function here - they're going to be going to different log groups.
logger.setLevel(logging.INFO)


def processing_handler(event, context):
    '''
    This finds the latest file in the s3 bucket, gets it from the bucket, and runs transformation functions on it.
    '''
    try:
        json_data = get_latest_file(event)
        #Once the json data has been accessed, it is split up for use by other functions.


        #JSON is already a dictionary, so this isn't dry coding
        # currency = json_data['currency']
        # payment = json_data['payment']
        # department = json_data['department']
        # design = json_data['design']
        # counterparty = json_data['counterparty']
        # purchase_order = json_data['purchase_order']
        # payment_type = json_data['payment_type']
        # sales_order = json_data['sales_order']
        # address = json_data['address']
        # staff = json_data['staff']
        # transaction = json_data['transaction']

        #These take a 
        #fact_table = create_fact_table(arg1, arg2)
        #dim_1 = create_dim_table_1(arg1)
        #....
        #dim_last = create_dim_table_last(arg1)

        #Converted_database = Parquet_conversion(fact_table, dim_1,...)
        #Or
        #Converted_fact_table = PC(fact_table)
        #Converted_dim_1 = PC(dim_1)

        #Once the tables have been created, this sends data into the processed bucket.

        # s3.put_object(
        #         Bucket='sandstone-processed-data',
        #         Key=f"{date}/{hour}-processed.json",
        #         # Body=Converted_database
        # )

    except KeyError:
        logger.error('There was an issue with the bucket data, please investigate.')
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'No object found - {s3_object_name}')
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error(f'Processed data bucket is missing')
        else:
            raise
    except InvalidFileTypeError:
        logger.error(f'File {s3_object_name} is not a JSON')
    except Exception as e:
        logger.error(e)
        raise RuntimeError



def get_latest_file(event):
    '''This is run within the handler to retrieve the object that triggered the most recent event.'''
    try:    
        event_names = get_object_path(event)
        s3_bucket_name = event_names['bucket']
        s3_object_name = event_names['object']
        logger.info(f'Bucket is {s3_bucket_name}')
        logger.info(f'Object is {s3_object_name}')

        if s3_object_name[-4:] != 'json':
            raise InvalidFileTypeError
        s3 = boto3.client('s3')

        #From my reading, the following code block, which finds the last-modified object in the bucket, is
        #redundant with the above code, which finds the name of the object that triggered the current eventbridge event
        #which should always be the most recent object.

        # response = s3.list_objects_v2(Bucket=s3_bucket_name)['Contents']
        # last_modified = lambda response: int(response['LastModified'].strftime('%s'))
        # latest_file = [response['Key'] for response in sorted(response, key=last_modified, reverse=True)][0]

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




# def get_table_from_dict(latest_data, choice):
#     '''This takes two arguments, representing the return from get_latest_file and the chosen table name respectively, and extracts the data for the table matching choice. It returns table data.'''
#     try:
#         return latest_data[choice]
#     except KeyError:
#         print('You entered an invalid table name')

def get_object_path(event_file):
    """Extracts bucket and object references from Records field of event."""
    return {'bucket': event_file['Records'][0]['s3']['bucket']['name'],\
         'object': event_file['Records'][0]['s3']['object']['key']}

class InvalidFileTypeError(Exception):
    '''Handles errors where file is not a json'''