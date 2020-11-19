import calendar
import datetime


def iter_next_days(n, start=None):
    if start is None:
        start = datetime.date.today()
    for i in range(n):
        yield start + datetime.timedelta(days=i)


def iter_days_of_next_months(n, start=None):
    if start is None:
        start = datetime.date.today()
    start = first_day_of_month(start)
    end = start
    for _ in range(n):
        end = next_month(end)
    end = end - datetime.timedelta(days=1)
    d = start
    while d <= end:
        yield d
        d = d + datetime.timedelta(days=1)


def first_day_of_month(now=None):
    if now is None:
        now = datetime.date.today()
    d = now.replace(day=1)
    return d


def last_day_of_month(now=None):
    if now is None:
        now = datetime.date.today()
    return next_month(first_day_of_month(now)) - datetime.timedelta(days=1)


def next_month(d):
    if d.month == 12:
        return d.replace(year=d.year + 1, month=1)
    else:
        return d.replace(month=d.month + 1)


def prev_month(d):
    if d.month == 1:
        return d.replace(year=d.year - 1, month=12)
    else:
        return d.replace(month=d.month - 1)


def weeknumber_to_date(year, week):
    str = '{year}-{week}-1'.format(year=year, week=week)
    return datetime.datetime.strptime(str, '%Y-%W-%w').date()


def date_to_weeknumber(d):
    return (int(x) for x in d.strftime('%Y-%W').split('-'))


def first_day_of_week(d):
    n = calendar.weekday(d.year, d.month, d.day)
    return d - datetime.timedelta(days=n)


def is_working_day(d):
    return 0 <= calendar.weekday(d.year, d.month, d.day) <= 4
