from unittest.mock import Mock, patch
from src.utils.get_table_from_dict import get_table_from_dict, get_latest_file
from moto import mock_s3
import json
import botocore
from time import sleep

@mock_s3
def test_get_latest_file_returns_correct():
    ''''''
    client = botocore.session.get_session().create_client('s3')
    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    val1 = {'last_ids': {'table1': 1,
                         'table2': 1}, 'moew': 'meow'}
    val2 = {'last_ids': {'table1': 2,
                         'table2': 2}, 'moew': 'meow'}

    client.put_object(
        Body=json.dumps(val1),
        Bucket='sandstone-ingested-data',
        Key='23-10-31/12-10.json',
    )
    sleep(10)

    client.put_object(
        Body=json.dumps(val2),
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-10.json',
    )
    output = get_latest_file()
    assert isinstance(output, dict)
    assert output == val2

@mock_s3
def test_get_table_from_dict():
    client = botocore.session.get_session().create_client('s3')

    currency_value = {
    "currency_id": [1, 2, 3],
    "currency_code": ["GBP", "USD", "EUR"],
    "created_at": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ],
    "last_updated": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ]
   }

    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    val1 = {'last_ids': {'table1': 1,
                         'table2': 1}, 'moew': 'meow'}
    val2 = {'last_ids': {'table1': 2,
                         'table2': 2},
            "currency": currency_value}

    client.put_object(
        Body=json.dumps(val1),
        Bucket='sandstone-ingested-data',
        Key='23-10-31/12-10.json',
    )
    sleep(10)

    client.put_object(
        Body=json.dumps(val2),
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-10.json',
    )
    output = get_table_from_dict(get_latest_file(), 'currency')
    assert output == currency_value

@mock_s3
def test_get_table_from_dict_handles_key_errors(capsys):
    client = botocore.session.get_session().create_client('s3')

    currency_value = {
    "currency_id": [1, 2, 3],
    "currency_code": ["GBP", "USD", "EUR"],
    "created_at": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ],
    "last_updated": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ]
   }

    client.create_bucket(
        Bucket='sandstone-ingested-data',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    val2 = {'last_ids': {'table1': 2,
                         'table2': 2},
            "currency": currency_value}
    client.put_object(
        Body=json.dumps(val2),
        Bucket='sandstone-ingested-data',
        Key='23-11-01/12-10.json',
    )
    get_table_from_dict(get_latest_file(), 'jfjfjj')
    captured = capsys.readouterr()
    assert captured.out == 'You entered an invalid table name\n'