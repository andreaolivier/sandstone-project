from src.utils.parquet_converter import parquet_converter
from unittest.mock import patch
from moto import mock_s3
import boto3
import botocore
import pytest
import os
from datetime import datetime
import awswrangler as wr
import pandas as pd
from pandas.testing import assert_frame_equal

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
def test_date_hour_tablename_correct():
    '''Testing that the parquet converter creates a new bucket object
    with correct date and time and tablename when passed multiple tables'''
    sample_design_data = {
        "department_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "department_name": [
            "Sales",
            "Purchasing",
            "Production",
            "Dispatch",
            "Finance",
            "Facilities",
            "Communications",
            "HR"
        ],
        "location": [
            "Manchester",
            "Manchester",
            "Leeds",
            "Leds",
            "Manchester",
            "Manchester",
            "Leeds",
            "Leeds"
        ],
        "manager": [
            "Richard Roma",
            "Naomi Lapaglia",
            "Chester Ming",
            "Mark Hanna",
            "Jordan Belfort",
            "Shelley Levene",
            "Ann Blake",
            "James Link"
        ],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ]
    }

    list_dict = [sample_design_data, sample_design_data]
    table_list = ['abc', 'def']
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-processed-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    with patch('src.utils.parquet_converter.dt') as dt:
        dt.today.return_value = datetime(
            2023, 11, 1, 12, 29, 7, 908653)

        parquet_converter(list_dict, table_list)
    response_1 = client.get_object(
        Bucket='sandstone-processed-data',
        Key='23-11-01/12-29/abc.parquet'
    )
    response_2 = client.get_object(
        Bucket='sandstone-processed-data',
        Key='23-11-01/12-29/def.parquet'
    )
    print(response_1)
    print(response_2)

    assert response_1 and response_2

@mock_s3
def test_creates_readable_parquet():
    '''Tests that parquet_converter creates
     a parquet file in the correct format'''

    sample_design_data = {
        "department_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "department_name": [
            "Sales",
            "Purchasing",
            "Production",
            "Dispatch",
            "Finance",
            "Facilities",
            "Communications",
            "HR"
        ],
        "location": [
            "Manchester",
            "Manchester",
            "Leeds",
            "Leds",
            "Manchester",
            "Manchester",
            "Leeds",
            "Leeds"
        ],
        "manager": [
            "Richard Roma",
            "Naomi Lapaglia",
            "Chester Ming",
            "Mark Hanna",
            "Jordan Belfort",
            "Shelley Levene",
            "Ann Blake",
            "James Link"
        ],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ]
    }

    list_dict = [sample_design_data]
    table_list = ['abc']
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-processed-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    with patch('src.utils.parquet_converter.dt') as dt:
        dt.today.return_value = datetime(
            2023, 11, 1, 12, 29, 7, 908653)

        parquet_converter(list_dict, table_list)
    df_expected = pd.DataFrame.from_dict(sample_design_data)
    test_path = "s3://sandstone-processed-data/23-11-01/12-29/"
    parquet_body = wr.s3.read_parquet(path=test_path, dataset=True)
    print(parquet_body.to_dict('tight'))
    assert df_expected.to_dict('tight') == parquet_body.to_dict('tight')

