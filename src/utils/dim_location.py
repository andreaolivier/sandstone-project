def to_dim_location(data):
    '''
    Formats data as required for revised database schema.

    args: data, a dict of table dicts
    
    returns: dim_location, a dict containing data needed for dim_location table
    '''
    columns_to_skip = ['address_id', 'created_at', 'last_updated']
    dim_location = {k: data['address'][k] for k in data['address'].keys() 
                    if k not in columns_to_skip}
    return dim_location
