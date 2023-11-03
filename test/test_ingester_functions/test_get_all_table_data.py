import os
from dotenv import load_dotenv
from pg8000.native import Connection
from src.ingestion import get_all_table_data

load_dotenv()


def test_get_all_table_data():
    """Test that all tables are returned during ingestion
        Asserts:
            list(data_keys): Ensures the returned table
            matches the expected tables
    """
    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    data = get_all_table_data(conn)
    data_keys = data.keys()

    assert list(data_keys) == ['last_ids',
                               'currency',
                               'payment',
                               'department',
                               'design',
                               'counterparty',
                               'purchase_order',
                               'payment_type',
                               'sales_order',
                               'address',
                               'staff',
                               'transaction']


def test_get_right_currency_table():
    """Test that currency table contains the right content
        Asserts:
            list(get_data['currency'].keys()): Ensures that currency table has
            the right column names
    """
    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    currency_table_columns = ['currency_id',
                              'currency_code',
                              'created_at',
                              'last_updated']
    get_data = get_all_table_data(conn)

    assert list(get_data['currency'].keys()) == currency_table_columns


def test_get_right_last_ids_table():
    """Test that last_ids table contains the right content
        Asserts:
            list(get_data['last_ids'].keys()): Ensures that last_ids table has
            the right column names
    """
    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    last_ids_table_columns = ['currency',
                              'payment',
                              'department',
                              'design',
                              'counterparty',
                              'purchase_order',
                              'payment_type',
                              'sales_order',
                              'address',
                              'staff',
                              'transaction']
    get_data = get_all_table_data(conn)

    assert list(get_data['last_ids'].keys()) == last_ids_table_columns


def test_get_right_payment_table():
    """Test that payment table contains the right content
        Asserts:
            list(get_data['payment'].keys()): Ensures that payment table has
            the right column names
    """
    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    payment_table_columns = ['payment_id',
                             'created_at',
                             'last_updated',
                             'transaction_id',
                             'counterparty_id',
                             'payment_amount',
                             'currency_id',
                             'payment_type_id',
                             'paid',
                             'payment_date',
                             'company_ac_number',
                             'counterparty_ac_number']
    get_data = get_all_table_data(conn)

    assert list(get_data['payment'].keys()) == payment_table_columns
