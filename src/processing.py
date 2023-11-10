from pg8000.native import Connection
from ingestion import get_table_data
import datetime as dt
from math import ceil
import os
import pandas as pd
import awswrangler as wr


def dim_counter_party(data):
    """
    The dim_counter_party function first checks if the input data is a dict.
    If yes, it creates the dimension table else it throws a type error
    """
    if not isinstance(data, dict):
        raise TypeError("Invalid data format")

    conn = Connection(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD']
    )
    address_data = get_table_data(conn, 'address')

    dim_counterparty = {
        "counterparty_id": data["counterparty"]["counterparty_id"],
        "counterparty_legal_name": data["counterparty"]
        ["counterparty_legal_name"],
        "counterparty_legal_address_line_1": [address_data
                                              ["address_line_1"]
                                              [i-1] for i in
                                              data["counterparty"]
                                              ["legal_address_id"]],
        "counterparty_legal_address_line2": [address_data
                                             ["address_line_2"]
                                             [i-1] for i in
                                             data["counterparty"]
                                             ["legal_address_id"]],
        "counterparty_legal_district": [address_data
                                        ["district"]
                                        [i-1] for i in
                                        data["counterparty"]
                                        ["legal_address_id"]],
        "counterparty_legal_city": [address_data
                                    ["city"]
                                    [i-1] for i in
                                    data["counterparty"]
                                    ["legal_address_id"]],
        "counterparty_legal_postal_code": [address_data
                                           ["postal_code"]
                                           [i-1] for i in
                                           data["counterparty"]
                                           ["legal_address_id"]],
        "counterparty_legal_country": [address_data
                                       ["country"]
                                       [i-1] for i in
                                       data["counterparty"]
                                       ["legal_address_id"]],
        "counterparty_legal_phone_number": [address_data
                                            ["phone"]
                                            [i-1] for i in
                                            data["counterparty"]
                                            ["legal_address_id"]]
    }

    return dim_counterparty


def get_currency_data(data):
    '''takes a dict of dicts as arguments and returns a dict
    with keys 'currency_id', 'currency_code' and 'currency_name'
    assigns a currency name by matching currency_code to key in curr_name'''
    curr_name = {
        "USD": "United States Dollar",
        "EUR": "Euro",
        "GBP": "British Pound Sterling",
    }
    currency = data['currency']
    currency_data = {
        'currency_id': currency['currency_id'],
        'currency_code': currency['currency_code'],
        'currency_name': [curr_name[i] for i in currency['currency_code']
                          for name in curr_name if i == name],
    }
    return currency_data


def to_dim_date():
    """
    Generates and formats dates from 01/01/20 to 01/01/29

    This will only need to run the first time, and will not be updated
    every time new data is ingested
    """
    dim_date = {}
    start_date = dt.datetime.strptime('01/01/20', '%d/%m/%y')
    all_dates = [start_date + dt.timedelta(days=i) for i in range(3650)]
    dim_date['date_id'] = [i.strftime('%Y-%m-%d') for i in all_dates]
    dim_date['year'] = [int(i.strftime('%Y')) for i in all_dates]
    dim_date['month'] = [int(i.strftime('%m')) for i in all_dates]
    dim_date['day'] = [int(i.strftime('%d')) for i in all_dates]
    # N.B: for day_of_week, 0 = Sunday
    dim_date['day_of_week'] = [int(i.strftime('%w')) for i in all_dates]
    dim_date['day_name'] = [i.strftime('%A') for i in all_dates]
    dim_date['month_name'] = [i.strftime('%B') for i in all_dates]
    dim_date['quarter'] = [ceil(int(i) / 3) for i in dim_date['month']]
    return dim_date


def make_new_design_table(big_dict):
    '''This takes the full data dictionary and returns a dictionary'''
    '''containing lists of the appropriate columns, '''
    '''maintaining the same structure otherwise.'''
    design_table = big_dict['design']

    design_columns = ['design_id', 'design_name', 'file_location', 'file_name']

    dim_design = {key: design_table[key] for key in design_columns}

    return dim_design


def to_dim_location(data):
    '''
    Formats data as required for revised database schema.

    args: data, a dict of table dicts

    returns: dim_location, a dict containing data needed for dim_location table
    '''
    column_mapping = {
        'address_id': 'location_id',
        'address_line_1': 'address_line_1',
        'address_line_2': 'address_line_2',
        'district': 'district',
        'city': 'city',
        'postal_code': 'postal_code',
        'country': 'country',
        'phone': 'phone'
    }
    dim_location = {column_mapping[k]: data['address'][k]
                    for k in column_mapping.keys()}
    return dim_location


def create_dim_staff(dict):
    try:
        conn = Connection(
            user=os.environ['DB_USER'],
            database=os.environ['DB_NAME'],
            port=os.environ['DB_PORT'],
            host=os.environ['DB_HOST'],
            password=os.environ['DB_PASSWORD']
        )
        dept_data = get_table_data(conn, 'department')
        dim_staff = {
            'staff_id': dict['staff']['staff_id'],
            'first_name': dict['staff']['first_name'],
            'last_name': dict['staff']['last_name'],
            'department_name': [dept_data['department_name'][id - 1]
                                for id in dict['staff']['department_id']],
            'location': [dept_data['location'][id - 1]
                         for id in dict['staff']['department_id']],
            'email_address': dict['staff']['email_address']
        }
        return (dim_staff)
    except KeyError:
        return ('Cannot find the specified key')
    except TypeError:
        return ('Passed input of incorrect type')
    except Exception as e:
        return (e)


def fact_sales_util(big_dict):
    """Returns the names of all the columns in the passed table from the
    connected PSQL database.
        Parameters:
            big_dict (dict): Table data from a database sorted by tables and
            columns.
    """
    salesorder = big_dict['sales_order']
    created_at = salesorder['created_at']
    last_updated = salesorder['last_updated']

    new_table = {
        'created_time': [date[11:] for date in created_at],
        'created_date': [date[:10] for date in created_at],
        'last_updated_time': [date[11:] for date in last_updated],
        'last_updated_date': [date[:10] for date in last_updated]
    }

    for key in salesorder.keys():
        if key not in ['created_at', 'last_updated'] and key not in new_table:
            new_table[key] = salesorder[key]

    return new_table


def parquet_converter(table_dicts, names_of_tables):
    '''This converts the inputted list of dictionaries to parquet files, and
    sends them into the sandstone-processed-data bucket on s3.
    Parameters:
        table_dicts: This is a list of fact and dim dictionaries created by
        the transformation functions.
        names_of_tables: This is a list of the names of the tables
        within the table_dicts.'''
    d = dt.datetime.today().strftime('%y-%m-%d')
    h = dt.datetime.today().strftime('%H-%M')
    for index, table in enumerate(table_dicts):
        table_name = names_of_tables[index]
        wr.s3.to_parquet(
            df=pd.DataFrame.from_dict(table),
            path=f's3://sandstone-processed-data/{d}/{h}/{table_name}.parquet'
        )
