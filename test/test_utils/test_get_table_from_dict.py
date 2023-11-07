from unittest.mock import Mock, patch
from src.utils.processing_handler import get_latest_file, InvalidFileTypeError
from moto import mock_s3
import json
import botocore
from time import sleep
import pytest
import logging


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
    output = get_latest_file(mock_event)
    assert isinstance(output, dict)
    assert output == val2


@mock_s3
def test_get_latest_file_raises_file_type_error(caplog):
    '''
    Tests that get_latest_file logs a filetype error correctly when the incoming data is in the wrong format.
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
        get_latest_file(mock_event)
        assert 'File 23-11-01/12-10.txt is not a JSON' in caplog.text

@mock_s3
def test_get_latest_file_raises_client_error(caplog):
    '''
    Tests that get_latest_file raises a client error when the event object key doesn't match incoming object.
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
            Key='23-11-01/12-.json',
        )
        output = get_latest_file(mock_event)
        assert 'No object found - 23-11-01/12-10.json' in caplog.text
