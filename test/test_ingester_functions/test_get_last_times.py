"""Tests for get_last_times function"""
import os
import json
import pytest
from moto import mock_s3
import boto3
import botocore
from ingestion import get_last_times


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
def test_get_last_times_returns_empty_dictionary_no_object():
    """Tests that get_last_times() returns an empty dictionary if there is no
    objects in the S3 bucket.
    """
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='tester',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    result = get_last_times(client, 'tester')
    assert result == {}


@mock_s3
def test_get_last_times_returns_dictionary_containing_last_ids():
    """Tests that get_last_times() returns a dictionary with all the last_ids
    from the latest S3 Object.
    """
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='tester',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    val1 = {'last_times': {'table1': '2020-01-01 00:00:00',
                           'table2': '2021-01-01 00:00:00'}, 'moew': 'meow'}
    val2 = {'last_times': {'table1': '2023-01-01 00:00:00',
                           'table2': '2024-01-01 00:00:00'}, 'moew': 'meow'}

    client.put_object(
        Body=json.dumps(val2),
        Bucket='tester',
        Key='23-12-31/12-10.json',
    )

    client.put_object(
        Body=json.dumps(val1),
        Bucket='tester',
        Key='23-11-01/12-10.json',
    )

    result = get_last_times(client, 'tester')
    assert result == {'table1': '2023-01-01 00:00:00',
                      'table2': '2024-01-01 00:00:00'}
