from processing import to_dim_location
import json

with open('./example_data/11-43.json') as f:
    test_data = json.load(f)


def test_output_table_has_correct_column_keys():
    formatted_data = to_dim_location(test_data)
    expected_columns = ['location_id', 'address_line_1', 'address_line_2',
                        'district', 'city', 'postal_code', 'country', 'phone']
    assert list(formatted_data.keys()) == expected_columns


def test_output_table_has_correct_number_of_values_in_columns():
    formatted_data = to_dim_location(test_data)
    expected_length = len(test_data['address']['address_id'])
    assert len(formatted_data['phone']) == expected_length
