from src.utils.make_new_design_table import make_new_design_table

import pytest
import json

@pytest.fixture
def sample_data_table():
    sample_data = {"design": {
        "design_id": [7, 8, 5, 4],
        "created_at": ["2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
            ],
        "design_name": ["Wooden", "Wooden", "Granite", "Granite"],
        "file_location": ["/usr/obj", "/usr", "/Network", "/usr/local/src"],
        "file_name": ["wooden-20211114-otpq.json",
            "wooden-20220717-npgz.json",
            "granite-20220419-b6n4.json",
            "granite-20220430-l5fs.json"],
        "last_updated": ["2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"]
    },
    'payment_type': {
        'payment_type_id': [],
        'payment_type_name': []
    }
    }
    return sample_data

@pytest.fixture
def sample_data_empty_table():
    sample_data = {"design": {
        "design_id": [],
        "created_at": [],
        "design_name": [],
        "file_location": [],
        "file_name": [],
        "last_updated": []
    },
    'payment_type': {
        'payment_type_id': [],
        'payment_type_name': []
    }
    }
    return sample_data

def test_design_table_returns_dict_of_lists(sample_data_table):
    output = make_new_design_table(sample_data_table)
    assert isinstance(output, dict)
    for i in output:
        assert isinstance(output[i], list)

def test_design_table_returns_correct_dict(sample_data_table):
    output = make_new_design_table(sample_data_table)
    assert output == {
        "design_id": [7, 8, 5, 4],
        "design_name": ["Wooden", "Wooden", "Granite", "Granite"],
        "file_location": ["/usr/obj", "/usr", "/Network", "/usr/local/src"],
        "file_name": ["wooden-20211114-otpq.json",
            "wooden-20220717-npgz.json",
            "granite-20220419-b6n4.json",
            "granite-20220430-l5fs.json"]
    }

def test_design_table_returns_empty_dict_when_no_data(sample_data_empty_table):
    output = make_new_design_table(sample_data_empty_table)
    assert output == {}