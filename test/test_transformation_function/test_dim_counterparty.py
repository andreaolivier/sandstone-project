import json
import pytest
from utils.dim_counterparty import dim_counter_party


def test_dim_counter_party_returns_a_dict():
    """
    Here we test to make sure that the returned value is a dict
    """
    with open('./test_data/11-43.json') as f:
        test_data = json.load(f)
    result = dim_counter_party(test_data)
    expected = dict
    assert isinstance(result, expected)


def test_dim_counter_party_returns_correct_values():
    """
    Here we test to make sure the dict keys are well formatted
    """
    with open('./test_data/11-43.json') as f:
        test_data = json.load(f)
    result = dim_counter_party(test_data)
    expected_columns = [
        "counterparty_id",
        "counterparty_legal_name",
        "counterparty_legal_address_line_1",
        "counterparty_legal_address_line2",
        "counterparty_legal_district",
        "counterparty_legal_city",
        "counterparty_legal_postal_code",
        "counterparty_legal_country",
        "counterparty_legal_phone_number"
    ]
    assert list(result.keys()) == expected_columns
    expected_address = '605 Haskell Trafficway'
    expected_zip = '99305-7380'
    assert result["counterparty_legal_address_line_1"][0] == expected_address
    assert result["counterparty_legal_postal_code"][-1] == expected_zip


def test_dim_counter_party_for_type_error():
    """
    We test here to make sure that the right data structure is passed in
    """
    with pytest.raises(TypeError) as err:
        dim_counter_party(["abc"])
    assert str(err.value) == "Invalid data format"
