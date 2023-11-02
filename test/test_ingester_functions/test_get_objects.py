"""Tests for get_objects function"""
import os
import pytest
from moto import mock_s3
import boto3
import botocore
from src.utils.ingestion import get_object_list


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
def test_get_objects_returns_an_empty_list_no_objects():
    """Test that get_objects() returns an empty list if there is no objects in
    the S3 Bucket.
    """
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='tester',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
        )

    result = get_object_list(client, 'tester')
    print(result)
    assert result == []


@mock_s3
def test_get_objects_returns_all_objects_from_bucket_in_list():
    """Test that get_objects() returns all the objects from a bucket in a list.
    """
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='tester',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
        )

    file_names = ['test1', 'test2', 'test3', 'test4']

    for file in file_names:
        client.put_object(
            Body='meow',
            Bucket='tester',
            Key=file,
        )

    result = get_object_list(client, 'tester')
    assert result == ['test1', 'test2', 'test3', 'test4']
