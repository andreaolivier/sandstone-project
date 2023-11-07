def create_dim_staff(dict):
    try:
      ids = dict['staff']['department_id']
      dept_ids = dict['department']['department_id']
      dept = dict['department']                                       
      dim_staff = {
  'staff_id': dict['staff']['staff_id'],
  'first_name': dict['staff']['first_name'],
  'last_name': dict['staff']['last_name'],
  'department_name': [dept['department_name'][dept_ids.index(id)] for id in ids],
  'location': [dept['location'][dept_ids.index(id)] for id in ids],
  'email_address': dict['staff']['email_address']
      }
      return(dim_staff)
    except KeyError:
       return('Cannot find the specified key')
    except TypeError:
       return('Passed input of incorrect type')
    except Exception as e:
       return(e)
    
big_dict = {
    "staff": {
    "staff_id": [
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
    ],
    "first_name": [
      "Jeremie",
      "Deron",
      "Jeanette",
      "Ana",
      "Magdalena",
      "Korey",
      "Raphael",
      "Oswaldo",
      "Brody",
      "Jazmyn",
      "Meda",
      "Imani",
      "Stan",
      "Rigoberto",
      "Tom",
      "Jett",
      "Irving",
      "Tomasa",
      "Pierre",
      "Flavio"
    ],
    "last_name": [
      "Franey",
      "Beier",
      "Erdman",
      "Glover",
      "Zieme",
      "Kreiger",
      "Rippin",
      "Bergstrom",
      "Ratke",
      "Kuhn",
      "Cremin",
      "Walker",
      "Lehner",
      "VonRueden",
      "Gutkowski",
      "Parisian",
      "O'Keefe",
      "Moore",
      "Sauer",
      "Kulas"
    ],
    "department_id": [
      2, 6, 6, 3, 8, 3, 2, 7, 2, 2, 5, 5, 4, 7, 3, 6, 3, 8, 2, 3
    ],
    "email_address": [
      "jeremie.franey@terrifictotes.com",
      "deron.beier@terrifictotes.com",
      "jeanette.erdman@terrifictotes.com",
      "ana.glover@terrifictotes.com",
      "magdalena.zieme@terrifictotes.com",
      "korey.kreiger@terrifictotes.com",
      "raphael.rippin@terrifictotes.com",
      "oswaldo.bergstrom@terrifictotes.com",
      "brody.ratke@terrifictotes.com",
      "jazmyn.kuhn@terrifictotes.com",
      "meda.cremin@terrifictotes.com",
      "imani.walker@terrifictotes.com",
      "stan.lehner@terrifictotes.com",
      "rigoberto.vonrueden@terrifictotes.com",
      "tom.gutkowski@terrifictotes.com",
      "jett.parisian@terrifictotes.com",
      "irving.o'keefe@terrifictotes.com",
      "tomasa.moore@terrifictotes.com",
      "pierre.sauer@terrifictotes.com",
      "flavio.kulas@terrifictotes.com"
    ],
    "created_at": [
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000"
    ],
    "last_updated": [
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000",
      "2022-11-03 14:20:51.563000"
    ]
  },
  "department": {
    "department_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "department_name": [
      "Sales",
      "Purchasing",
      "Production",
      "Dispatch",
      "Finance",
      "Facilities",
      "Communications",
      "HR"
    ],
    "location": [
      "Manchester",
      "Manchester",
      "Leeds",
      "Leds",
      "Manchester",
      "Manchester",
      "Leeds",
      "Leeds"
    ],
    "manager": [
      "Richard Roma",
      "Naomi Lapaglia",
      "Chester Ming",
      "Mark Hanna",
      "Jordan Belfort",
      "Shelley Levene",
      "Ann Blake",
      "James Link"
    ],
    "created_at": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ],
    "last_updated": [
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000",
      "2022-11-03 14:20:49.962000"
    ]
  },
}

print(create_dim_staff([]))
