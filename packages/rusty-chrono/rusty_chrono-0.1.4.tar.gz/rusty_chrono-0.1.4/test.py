import datetime
from rusty_chrono import datediff, datediff_from_pydate, datediff_from_pydatetime

fraction = 'MONTH'
one_week = datetime.timedelta(weeks=15)

end_date = datetime.date.today()
start_date = end_date - one_week

end_datetime = datetime.datetime.now()
start_datetime = end_datetime - one_week

print(datediff_from_pydate(start_date, end_date, fraction))
print(datediff_from_pydatetime(start_datetime, end_datetime, fraction))
print(datediff("2023-02-01", "2023-05-17", "%Y-%m-%d", "MONTH"))
print(datediff("2023-02-01 11:54", "2023-05-17 11:54", "%Y-%m-%d %H:%M", "MONTH", "datetime"))
print(datediff("2023-02-01", "2023-05-17", "%Y-%m-%d", "DAY"))