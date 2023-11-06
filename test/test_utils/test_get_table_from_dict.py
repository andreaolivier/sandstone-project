from unittest.mock import Mock, patch
from src.utils.get_table_from_dict import get_table_from_dict


def test_data_frame_created():
    with patch('s3.list_objects_v2', create=True) as mock_req:
        mock_req.return_value = {'test': 'sandstone-project/test/test_utils/mock.json'}
        output = get_table_from_dict()
        assert output == 
    