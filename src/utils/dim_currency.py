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
        'currency_name': [
            curr_name[i] for i in currency['currency_code'] for name in curr_name if i == name],
    }
    return currency_data
