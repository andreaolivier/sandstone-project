"""Tests for check_for_new_values function"""
from src.ingestion import check_for_new_values


def test_check_for_new_values_returns_false_no_new_values():
    """Test that check_for_new_values() returns false when table dictionaries
    have no data.
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

    result = check_for_new_values(data)

    print(result)
    assert result is False


def test_check_for_new_values_returns_true_new_values():
    """Test that check_for_new_values() returns false when table dictionaries
    have no data.
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

    result = check_for_new_values(data)

    print(result)
    assert result is True
