"""Temporary File for fact_staff_util"""


def fact_staff_util(big_dict):
    """Returns the names of all the columns in the passed table from the
    connected PSQL database.
        Parameters:
            big_dict (dict): Table data from a database sorted by tables and
            columns.
    """
    salesorder = big_dict['sales_order']
    created_at = salesorder['created_at']
    last_updated = salesorder['last_updated']

    if salesorder['sales_order_id'] == []:
        return {}

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
