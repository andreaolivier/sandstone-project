import datetime as dt
from math import ceil

def dim_date():
    """
    Generates and formats dates from 01/01/20 to 01/01/29

    This will only need to run the first time, and will not be updated
    every time new data is ingested
    """
    dim_date = {}
    start_date = dt.datetime.strptime('01/01/20', '%d/%m/%y')
    all_dates = [start_date + dt.timedelta(days=i) for i in range(3650)]
    dim_date['date_id'] = [i.strftime('%Y-%m-%d') for i in all_dates]
    dim_date['year'] = [int(i.strftime('%Y')) for i in all_dates]
    dim_date['month'] = [int(i.strftime('%m')) for i in all_dates]
    dim_date['day'] = [int(i.strftime('%d')) for i in all_dates]
    # N.B: for day_of_week, 0 = Sunday
    dim_date['day_of_week'] = [int(i.strftime('%w')) for i in all_dates]
    dim_date['day_name'] = [i.strftime('%A') for i in all_dates]
    dim_date['month_name'] = [i.strftime('%B') for i in all_dates]
    dim_date['quarter'] = [ceil(int(i)/3) for i in dim_date['month']]
    return dim_date
