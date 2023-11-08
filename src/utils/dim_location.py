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
