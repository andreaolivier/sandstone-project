import pandas as pd
import awswrangler as wr
from datetime import datetime as dt


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
