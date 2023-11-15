from processing import to_dim_staff


def test_returns_dict_with_no_info_when_passed_dict_of_dicts_with_no_info():
    data = {
        "staff": {
            "staff_id": [],
            "first_name": [],
            "last_name": [],
            "department_id": [],
            "email_address": [],
            "created_at": [],
            "last_updated": []
        },
        "department": {
            "department_id": [],
            "department_name": [],
            "location": [],
            "manager": [],
            "created_at": [],
            "last_updated": []
        },
    }
    result = {'staff_id': [], 'first_name': [], 'last_name': [],
              'department_name': [], 'location': [], 'email_address': []}

    assert to_dim_staff(data) == result


def test_returns_empty_dict_when_passed_dict_with_only_dept_info():
    data = {
        "staff": {
            "staff_id": [],
            "first_name": [],
            "last_name": [],
            "department_id": [],
            "email_address": [],
            "created_at": [],
            "last_updated": []
        },
        "department": {
            "department_id": [1, 2, 3, 4],
            "department_name": ['Marketing', 'Retail', 'DevOps', 'Data'],
            "location": ['Manchester', 'London', 'Oxford', 'Edinburgh'],
            "manager": [],
            "created_at": [],
            "last_updated": []
        },
    }

    result = {'staff_id': [], 'first_name': [], 'last_name': [],
              'department_name': [], 'location': [], 'email_address': []}

    assert to_dim_staff(data) == result


def test_returns_dict_with_info_when_passed_dict_with_only_staff_info():

    data = {
        "staff": {
            "staff_id": [1, 2, 3],
            "first_name": ['John', 'Pablo', 'Andrea'],
            "last_name": ['M', 'B', 'O'],
            "department_id": [2, 4, 3],
            "email_address": ['john@', 'pablo@', 'andrea@'],
            "created_at": [],
            "last_updated": []
        },
        "department": {
            "department_id": [],
            "department_name": [],
            "location": [],
            "manager": [],
            "created_at": [],
            "last_updated": []
        },
    }

    result = {
        'staff_id': [1, 2, 3],
        'first_name': ['John', 'Pablo', 'Andrea'],
        'last_name': ['M', 'B', 'O'],
        'department_name': ['Purchasing', 'Dispatch', 'Production'],
        'location': ['Manchester', 'Leds', 'Leeds'],
        'email_address': ['john@', 'pablo@', 'andrea@']}

    assert to_dim_staff(data) == result


def test_returns_error_if_passed_incorrect_input():
    assert to_dim_staff({}) == 'Cannot find the specified key'
    assert to_dim_staff([]) == 'Passed input of incorrect type'


def test_does_not_mutate_input_dict():
    data = {
        "staff": {
            "staff_id": [1, 2, 3],
            "first_name": ['John', 'Pablo', 'Andrea'],
            "last_name": ['M', 'B', 'O'],
            "department_id": [2, 4, 3],
            "email_address": ['john@', 'pablo@', 'andrea@'],
            "created_at": [],
            "last_updated": []
        },
        "department": {
            "department_id": [1, 2, 3, 4],
            "department_name": ['Marketing', 'Retail', 'DevOps', 'Data'],
            "location": ['Manchester', 'London', 'Oxford', 'Edinburgh'],
            "manager": [],
            "created_at": [],
            "last_updated": []
        },
    }
    to_dim_staff(data)
    assert data == {
        "staff": {
            "staff_id": [1, 2, 3],
            "first_name": ['John', 'Pablo', 'Andrea'],
            "last_name": ['M', 'B', 'O'],
            "department_id": [2, 4, 3],
            "email_address": ['john@', 'pablo@', 'andrea@'],
            "created_at": [],
            "last_updated": []
        },
        "department": {
            "department_id": [1, 2, 3, 4],
            "department_name": ['Marketing', 'Retail', 'DevOps', 'Data'],
            "location": ['Manchester', 'London', 'Oxford', 'Edinburgh'],
            "manager": [],
            "created_at": [],
            "last_updated": []
        },
    }
