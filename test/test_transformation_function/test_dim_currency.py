from processing import to_dim_currency

TEST_DATA = {"currency": {
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
    assert list(to_dim_currency(TEST_DATA).keys()) == [
        "currency_id", "currency_code", "currency_name"]


def test_dict_has_3_id_and_3_code():
    assert len(to_dim_currency(TEST_DATA)['currency_id']) == 3
    assert len(to_dim_currency(TEST_DATA)['currency_code']) == 3
    assert len(to_dim_currency(TEST_DATA)['currency_name']) == 3


def test_get_currency_data_returns_dict():
    assert isinstance(to_dim_currency(TEST_DATA), dict)
