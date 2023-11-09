"""
The dim_counter_party function takes in a dict of dict
then transforms it into a dimensions table
"""
from pg8000.native import Connection
from src.ingestion import get_table_data
import os
=======

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
