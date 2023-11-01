"""Tests for check_for_new_values function"""
from src.utils.ingestion import get_column_names
from pg8000.native import Connection
import os
from dotenv import load_dotenv

load_dotenv()


def test_get_column_names_returns_a_list_of_all_column_names():
    """Test that get_column_names() returns a list of columns names of
    table_name passed .
    """
    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    result = get_column_names(conn, 'currency')
    result2 = get_column_names(conn, 'payment_type')

    assert result == ['currency_id', 'currency_code',
                      'created_at', 'last_updated']
    print(result2)
    assert result2 == ['payment_type_id',
                       'payment_type_name', 'created_at', 'last_updated']
