from utils.dim_currency import get_currency_data

TEST_INPUT_DATA = {"currency": {
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
  }}

def test_dict_has_correct_keys():
    assert list(get_currency_data(TEST_INPUT_DATA).keys()) == ["currency_id", "currency_code", "currency_name"]

def test_dict_has_3_id_and_3_code():
    assert len(get_currency_data(TEST_INPUT_DATA)['currency_id']) is 3
    assert len(get_currency_data(TEST_INPUT_DATA)['currency_code']) is 3
    assert len(get_currency_data(TEST_INPUT_DATA)['currency_name']) is 3

def test_get_currency_data_returns_dict():
    assert isinstance(get_currency_data(TEST_INPUT_DATA), dict)



