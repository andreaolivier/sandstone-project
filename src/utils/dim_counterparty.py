"""
The dim_counter_party function takes in a dict of dict
then transforms it into a dimensions table
"""


def dim_counter_party(data):
    """
    The dim_counter_party function first checks if the input data is a dict.
    If yes, it creates the dimension table else it throws a type error
    """
    if not isinstance(data, dict):
        raise TypeError("Invalid data format")
    dim_counterparty = {
        "counterparty_id": data["counterparty"]["counterparty_id"],
        "counterparty_legal_name": data["counterparty"]
        ["counterparty_legal_name"],
        "counterparty_legal_address_line_1": [data["address"]
                                              ["address_line_1"]
                                              [i-1] for i in
                                              data["counterparty"]
                                              ["legal_address_id"]],
        "counterparty_legal_address_line2": [data["address"]
                                             ["address_line_2"]
                                             [i-1] for i in
                                             data["counterparty"]
                                             ["legal_address_id"]],
        "counterparty_legal_district": [data["address"]
                                        ["district"]
                                        [i-1] for i in
                                        data["counterparty"]
                                        ["legal_address_id"]],
        "counterparty_legal_city": [data["address"]
                                    ["city"]
                                    [i-1] for i in
                                    data["counterparty"]
                                    ["legal_address_id"]],
        "counterparty_legal_postal_code": [data["address"]
                                           ["postal_code"]
                                           [i-1] for i in
                                           data["counterparty"]
                                           ["legal_address_id"]],
        "counterparty_legal_country": [data["address"]
                                       ["country"]
                                       [i-1] for i in
                                       data["counterparty"]
                                       ["legal_address_id"]],
        "counterparty_legal_phone_number": [data["address"]
                                            ["phone"]
                                            [i-1] for i in
                                            data["counterparty"]
                                            ["legal_address_id"]]
    }

    return dim_counterparty
