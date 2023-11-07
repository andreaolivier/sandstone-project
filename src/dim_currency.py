def get_currency_data(data):
    '''takes a dict of dicts as arguments and returns a dict
    with keys 'currency_id' and 'currency_code' '''
    currency = data['currency']
    currency_data = {'currency_id': currency['currency_id'],
                    'currency_code': currency['currency_code'],
                    }
    return currency_data

