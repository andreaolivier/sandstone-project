from processing import dim_date
import json

with open('./example_data/11-43.json') as f:
    test_data = json.load(f)


def test_generates_10_years_worth_of_dates():
    dates = dim_date()
    expected_years = [2020 + i for i in range(10)]
    assert len(dates['year']) == 365 * 10
    assert [*set(dates['year'])] == expected_years


def test_contains_correct_columns():
    dates = dim_date()
    columns = list(dates.keys())
    expected_columns = ['date_id', 'year', 'month', 'day', 'day_of_week',
                        'day_name', 'month_name', 'quarter']
    assert columns == expected_columns


def test_calculates_quarter_correctly():
    dates = dim_date()
    months_in_Q1 = set(
        [dates['month'][i] for i in range(len(dates['month']))
         if dates['quarter'][i] == 1])
    months_in_Q2 = set(
        [dates['month'][i] for i in range(len(dates['month']))
         if dates['quarter'][i] == 2])
    months_in_Q3 = set(
        [dates['month'][i] for i in range(len(dates['month']))
         if dates['quarter'][i] == 3])
    months_in_Q4 = set(
        [dates['month'][i] for i in range(len(dates['month']))
         if dates['quarter'][i] == 4])
    assert months_in_Q1 == set([1, 2, 3])
    assert months_in_Q2 == set([4, 5, 6])
    assert months_in_Q3 == set([7, 8, 9])
    assert months_in_Q4 == set([10, 11, 12])
