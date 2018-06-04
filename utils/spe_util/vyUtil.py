from datetime import datetime, timedelta
import time

def date_to_stamp(date):
    d_datetime = time.strptime(date, '%Y-%m-%dT%H:%M:%S')
    d_stamp = time.mktime(d_datetime)
    return d_stamp

def format_duration(mins):
    hh = str(mins // 60).rjust(2, '0')
    mm = str(mins - int(hh) * 60).rjust(2, '0')
    return "%s:%s" % (hh, mm)

def analysisData(data):
    p = data.split(':')
    fromTo = p[0].split('-')
    dep = fromTo[0]
    to = fromTo[1]
    dt = p[1]
    days = p[2]
    return (dt, dep, to, days)

def get_real_date(date_str, diff_days):
    date_datetime = datetime.strptime(date_str, '%Y%m%d')
    days = timedelta(days=diff_days)
    date_datetime += days
    return date_datetime.strftime('%Y-%m-%d')

if __name__ == '__main__':
    # print(date_to_stamp("2018-04-27T19:45:00"))
    print(format_duration(3))