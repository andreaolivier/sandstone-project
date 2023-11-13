from processing_handler import (
    get_latest_file,
    InvalidFileTypeError,
    processing_handler)
from freezegun import freeze_time
from moto import mock_s3
import json
import botocore
import logging
import os
import pytest


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@mock_s3
def test_get_latest_file_returns_dictionary():
    '''
    Tests that get_latest_file returns a dictionary.
    '''
    mock_event = {
        "Records": [
            {
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "MyLambdaTrigger",
                    "bucket": {
                        "name": "sandstone-ingested-data",
                        "ownerIdentity": {
                            "principalId": "A3NL1KOZZKExample"
                        },
                    },
                    "object": {
                        "key": "23-11-01/12-10.json",

                    }
                }
            }
        ]
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    val2 = {'last_ids': {'table1': 2,
                         'table2': 2}, 'moew': 'meow'}

    client.put_object(
        Body=json.dumps(val2),
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-10.json',
    )
    output = get_latest_file(mock_event, client)
    assert isinstance(output, dict)
    assert output == val2


@mock_s3
def test_get_latest_file_raises_file_type_error(caplog):
    '''
    Tests that get_latest_file logs a filetype error correctly when the
    incoming data is in the wrong format.
    '''
    with caplog.at_level(logging.ERROR):
        mock_event = {
            "Records": [
                {
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "MyLambdaTrigger",
                        "bucket": {
                            "name": "sandstone-ingested-data",
                            "ownerIdentity": {
                                "principalId": "A3NL1KOZZKExample"
                            },
                        },
                        "object": {
                            "key": "23-11-01/12-10.txt",


                        }
                    }
                }
            ]
        }

        client = botocore.session.get_session().create_client('s3')
        client.create_bucket(
            Bucket='sandstone-ingested-data',
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
        )

        val2 = 'mock2'

        client.put_object(
            Body=json.dumps(val2),
            Bucket='sandstone-ingested-data',
            Key='23-11-01/12-10.txt',
        )
        try:
            get_latest_file(mock_event, client)
            assert False
        except InvalidFileTypeError:
            assert True

# @mock_s3
# def test_get_latest_file_raises_client_error(caplog):
#     '''
#     Tests that get_latest_file raises a client error when the event object
#     key doesn't match incoming object.
#     '''
#     with caplog.at_level(logging.ERROR):
#         mock_event = {
#     "Records": [
#         {
#         "s3": {
#             "s3SchemaVersion": "1.0",
#             "configurationId": "MyLambdaTrigger",
#             "bucket": {
#             "name": "sandstone-ingested-data",
#             "ownerIdentity": {
#                 "principalId": "A3NL1KOZZKExample"
#             },
#             },
#             "object": {
#             "key": "23-11-01/12-10.json",

#             }
#         }
#         }
#     ]
#     }

#         client = botocore.session.get_session().create_client('s3')
#         client.create_bucket(
#             Bucket='sandstone-ingested-data',
#             CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
#         )
#         val2 = {'last_ids': {'table1': 2,
#                             'table2': 2}, 'moew': 'meow'}

#         client.put_object(
#             Body=json.dumps(val2),
#             Bucket='sandstone-ingested-data',
#             Key='23-11-01/12-.json',
#         )
#         output = get_latest_file(mock_event)
#         assert 'No object found - 23-11-01/12-10.json' in caplog.text


@mock_s3
@freeze_time("2022-11-09T15:00:00.0")
def test_processing_handler_creates_correct_tables(aws_credentials):
    mock_event = {
        "Records": [
            {
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "MyLambdaTrigger",
                    "bucket": {
                        "name": "sandstone-ingested-data",
                        "ownerIdentity": {
                            "principalId": "A3NL1KOZZKExample"
                        },
                    },
                    "object": {
                        "key": "22-11-09/15-10.json",

                    }
                }
            }
        ]
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    with open('./example_data/11-43.json') as f:
        ingested_data = json.load(f)
    client.put_object(
        Body=json.dumps(ingested_data),
        Bucket='sandstone-ingested-data',
        Key='22-11-09/15-10.json',
    )

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-processed-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    processing_handler(mock_event, '')

    response = client.list_objects_v2(
        Bucket="sandstone-processed-data",
        )
    print(response)
    table_expected = [
        '22-11-09/15-00/dim_counterparty.parquet',
        '22-11-09/15-00/dim_currency.parquet',
        '22-11-09/15-00/dim_date.parquet',
        '22-11-09/15-00/dim_design.parquet',
        '22-11-09/15-00/dim_location.parquet',
        '22-11-09/15-00/dim_staff.parquet',
        '22-11-09/15-00/fact_sales_order.parquet'
        ]
    table_list = [table['Key'] for table in response["Contents"]]

    for table in table_list:
        assert table in table_expected


@mock_s3
@freeze_time("2022-11-09T15:00:00.0")
def test_processing_handler_raises_file_type_error(aws_credentials, caplog):
    caplog.set_level(logging.ERROR)
    mock_event = {
        "Records": [
            {
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "MyLambdaTrigger",
                    "bucket": {
                        "name": "sandstone-ingested-data",
                        "ownerIdentity": {
                            "principalId": "A3NL1KOZZKExample"
                        },
                    },
                    "object": {
                        "key": "22-11-09/15-10.py",

                    }
                }
            }
        ]
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    ingested_data = ["This", "is", "not", "correct", "."]

    client.put_object(
        Body=json.dumps(ingested_data),
        Bucket='sandstone-ingested-data',
        Key='22-11-09/15-10.py',
    )

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-processed-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    processing_handler(mock_event, '')
    assert "File is not a JSON" in caplog.text


@mock_s3
@freeze_time("2022-11-09T15:00:00.0")
def test_processing_handler_raises_bucket_error(aws_credentials, caplog):
    caplog.set_level(logging.ERROR)
    mock_event = {
        "Records": [
            {
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "MyLambdaTrigger",
                    "bucket": {
                        "name": "sandstone-ingested-data",
                        "ownerIdentity": {
                            "principalId": "A3NL1KOZZKExample"
                        },
                    },
                    "object": {
                        "key": "22-11-09/15-10.py",

                    }
                }
            }
        ]
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    ingested_data = ["This", "is", "not", "correct", "."]

    client.put_object(
        Body=json.dumps(ingested_data),
        Bucket='sandstone-ingested-data',
        Key='22-11-09/15-10.py',
    )

    processing_handler(mock_event, '')
    assert "Processed data bucket is missing" in caplog.text