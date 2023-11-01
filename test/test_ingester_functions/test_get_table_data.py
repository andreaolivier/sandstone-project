from src.utils.ingestion import get_table_data
from pg8000.native import Connection
from unittest.mock import patch

class Conn:
    def __init__(self):
        self.name = 'fake connection'
    def run(self, value):
        return ''
    
class Conn2:
    def __init__(self):
        self.name = 'fake connection'
    def run(self, value):
        return [['blabla', 'hey'], ['bleble', 'ho']]


def test_returns_empty_dict_if_no_data():
    dummy = Conn()
    with patch('src.utils.ingestion.get_column_names',return_value=['cheese', 'meow']):
        assert get_table_data(dummy, 'hello') == {'cheese': [], 'meow': [] }

def test_return_dictionary_with_data_if_data():
    dummy = Conn2()
    with patch('src.utils.ingestion.get_column_names',return_value=['cheese', 'meow']):
        assert get_table_data(dummy, 'hello') == {'cheese': ['blabla', 'bleble'], 'meow': ['hey', 'ho'] }




