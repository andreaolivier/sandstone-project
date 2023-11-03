"""Tests for ingestion_handler function"""
import os
import json
import pytest
from unittest.mock import patch
from moto import mock_s3
import boto3
import botocore
from datetime import datetime
from src.ingester import ingestion_handler


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def s3(aws_credentials):
    with mock_s3:
        yield boto3.client("s3", 'eu-west-2')


@mock_s3
def test_ingestion_handler_creates_object_if_bucket_empty_with_data():
    """Test that ingestion_handler() creates a new S3 Object with database
    data in bucket when the bucket is empty.
    """
    data = {
        "last_ids": {
            "currency": 0,
            "payment": 0,
            "department": 0,
            "design": 0,
            "counterparty": 0,
            "purchase_order": 0,
            "payment_type": 0,
            "sales_order": 0,
            "address": 0,
            "staff": 0,
            "transaction": 0
        },
        "currency": {
            "currency_id": [],
            "currency_code": [],
            "created_at": [],
            "last_updated": []
        },
        "design": {
            "design_id": [],
            "created_at": [],
            "design_name": ['Vale'],
            "file_location": [],
            "file_name": [],
            "last_updated": [123123, 32423, 321]
        },
        "payment_type": {
            "payment_type_id": [],
            "payment_type_name": [],
            "created_at": ['MORE VALUES'],
            "last_updated": []
        }
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    with patch('src.ingester.get_all_table_data') as get_table:
        with patch('src.ingester.dt') as dt:
            dt.today.return_value = datetime(
                2023, 11, 1, 12, 29, 7, 908653)

            get_table.return_value = data
            ingestion_handler()

    s3_response = client.get_object(
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-29.json'
    )

    file_content = s3_response.get('Body').read()
    json_content = json.loads(file_content)
    print(data)
    print(json_content)
    assert data == json_content


@mock_s3
def test_creates_s3_object_if_bucket_is_empty_with_database_data():
    """Test that ingestion_handler() doesn't create new object when there is
    no new data.
    """
    data = {
        "last_ids": {
            "currency": 0,
            "payment": 0,
            "department": 0,
            "design": 0,
            "counterparty": 0,
            "purchase_order": 0,
            "payment_type": 0,
            "sales_order": 0,
            "address": 0,
            "staff": 0,
            "transaction": 0
        },
        "currency": {
            "currency_id": [],
            "currency_code": [],
            "created_at": [],
            "last_updated": []
        },
        "design": {
            "design_id": [],
            "created_at": [],
            "design_name": [],
            "file_location": [],
            "file_name": [],
            "last_updated": []
        },
        "payment_type": {
            "payment_type_id": [],
            "payment_type_name": [],
            "created_at": [],
            "last_updated": []
        }
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    with patch('src.ingester.get_all_table_data') as get_table:
        with patch('src.ingester.dt') as dt:
            dt.today.return_value = datetime(
                2023, 11, 1, 12, 29, 7, 908653)

            get_table.return_value = data
            ingestion_handler()
    try:
        client.get_object(
            Bucket='sandstone-ingested-data',
            Key='23-11-01/12-29.json'
        )
        assert False
    except client.exceptions.NoSuchKey:
        assert True


@mock_s3
def test_creates_s3_object_if_bucket_has_objects_with_database_data_with_obj():
    """Test that ingestion_handler() creates new object when there is new data
    and there is existing object with data.
    """
    data = {
        "last_ids": {
            "currency": 0,
            "payment": 0,
            "department": 0,
            "design": 0,
            "counterparty": 0,
            "purchase_order": 0,
            "payment_type": 0,
            "sales_order": 0,
            "address": 0,
            "staff": 0,
            "transaction": 0
        },
        "currency": {
            "currency_id": [1, 2, 3],
            "currency_code": [0, 0, 0],
            "created_at": [0, 0, 0],
            "last_updated": [0, 0, 0]
        },
        "design": {
            "design_id": [1, 2],
            "created_at": [],
            "design_name": [],
            "file_location": [],
            "file_name": [],
            "last_updated": []
        },
        "payment_type": {
            "payment_type_id": [1, 2],
            "payment_type_name": [],
            "created_at": [],
            "last_updated": []
        }
    }
    data2 = {
        "last_ids": {
            "currency": 0,
            "payment": 0,
            "department": 0,
            "design": 0,
            "counterparty": 0,
            "purchase_order": 0,
            "payment_type": 0,
            "sales_order": 0,
            "address": 0,
            "staff": 0,
            "transaction": 0
        },
        "currency": {
            "currency_id": [],
            "currency_code": [],
            "created_at": [],
            "last_updated": []
        },
        "design": {
            "design_id": [],
            "created_at": [],
            "design_name": [],
            "file_location": [],
            "file_name": [],
            "last_updated": []
        },
        "payment_type": {
            "payment_type_id": [3, 4],
            "payment_type_name": [],
            "created_at": [],
            "last_updated": []
        }
    }

    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    with patch('src.ingester.get_all_table_data') as get_table:
        with patch('src.ingester.dt') as dt:
            dt.today.return_value = datetime(
                2023, 11, 1, 12, 29, 7, 908653)
            get_table.return_value = data

            ingestion_handler()

            dt.today.return_value = datetime(
                2023, 11, 1, 12, 35, 7, 908653)
            get_table.return_value = data2

            ingestion_handler()

    response = client.list_objects_v2(Bucket='sandstone-ingested-data')
    file_names = [bucket_obj['Key']
                  for bucket_obj in response['Contents']]

    assert file_names == ['23-11-01/12-29.json', '23-11-01/12-35.json']

    s3_response = client.get_object(
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-35.json'
    )

    file_content = s3_response.get('Body').read()
    json_content = json.loads(file_content)

    assert json_content == data2
