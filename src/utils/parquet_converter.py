import pandas as pd
import awswrangler as wr
from datetime import datetime as dt



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

def parquet_converter(table_dicts, names_of_tables):
    '''This converts the inputted list of dictionaries to parquet files, and 
    sends them into the sandstone-processed-data bucket on s3.
    Parameters: 
        table_dicts: This is a list of fact and dim dictionaries created by
        the transformation functions.
        names_of_tables: This is a list of the names of the tables 
        within the table_dicts.'''
    d = dt.today().strftime('%y-%m-%d')
    h = dt.today().strftime('%H-%M')
    for index, table in enumerate(table_dicts):
        table_name = names_of_tables[index]
        wr.s3.to_parquet(
            df=pd.DataFrame.from_dict(table),
            path=f's3://sandstone-processed-data/{d}/{h}/{table_name}.parquet'
            )
    

#     dataframe.to_parquet('test.parquet', index=False)
#     # print(pd.read_parquet('test.parquet'))
