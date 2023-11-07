import pandas as pd

data = {
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
}


dataframe = pd.DataFrame.from_dict(data)
dataframe.to_parquet('test.parquet', index=False)
print(pd.read_parquet('test.parquet'))

def parquet_converter(dict):
    dataframe = pd.DataFrame.from_dict(dict)
    dataframe.to_parquet('test.parquet', index=False)
    # print(pd.read_parquet('test.parquet'))
