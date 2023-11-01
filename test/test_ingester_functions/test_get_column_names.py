"""Tests for check_for_new_values function"""
from src.utils.ingestion import get_column_names
from src.ingester import get_connection


def test_get_column_names_returns_a_list_of_all_column_names():
    """Test that get_column_names() returns a list of columns names of
    table_name passed .
    """
    conn = get_connection()
    result = get_column_names(conn, 'currency')
    result2 = get_column_names(conn, 'payment_type')

    assert result == ['currency_id', 'currency_code',
                      'created_at', 'last_updated']
    print(result2)
    assert result2 == ['payment_type_id',
                       'payment_type_name', 'created_at', 'last_updated']
