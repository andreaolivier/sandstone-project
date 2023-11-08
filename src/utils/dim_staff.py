from pg8000.native import Connection
from src.ingestion import get_table_data
import os

def create_dim_staff(dict):
    try:
        conn = Connection(
            user=os.environ['DB_USER'],
            database=os.environ['DB_NAME'],
            port=os.environ['DB_PORT'],
            host=os.environ['DB_HOST'],
            password=os.environ['DB_PASSWORD']
        )
        dept_data = get_table_data(conn, 'department')
        dim_staff = {
            'staff_id': dict['staff']['staff_id'],
            'first_name': dict['staff']['first_name'],
            'last_name': dict['staff']['last_name'],
            'department_name': [dept_data['department_name'][id - 1] 
                                for id in dict['staff']['department_id']],
            'location': [dept_data['location'][id - 1] 
                         for id in dict['staff']['department_id']],
            'email_address': dict['staff']['email_address']
        }
        return (dim_staff)
    except KeyError:
        return ('Cannot find the specified key')
    except TypeError:
        return ('Passed input of incorrect type')
    except Exception as e:
        return (e)
