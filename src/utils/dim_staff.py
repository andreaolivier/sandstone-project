def create_dim_staff(dict):
    try:                                  
      dim_staff = {
  'staff_id': dict['staff']['staff_id'],
  'first_name': dict['staff']['first_name'],
  'last_name': dict['staff']['last_name'],
  'department_name': [dict['department']['department_name'][id-1] for id in dict['staff']['department_id']],
  'location': [dict['department']['location'][id-1] for id in dict['staff']['department_id']],
  'email_address': dict['staff']['email_address']
      }
      return(dim_staff)
    except KeyError:
       return('Cannot find the specified key')
    except TypeError:
       return('Passed input of incorrect type')
    except Exception as e:
       return(e)