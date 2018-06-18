#encoding:utf-8
import time, requests,logging, sys, random
from datetime import datetime, timedelta
sys.path.append('..') # 测试专用
from myspiders import settings
import json

def strip_item(item):
    for k, v in item.items():
        if isinstance(v, str):
            item[k] = v.strip()
    return item

# 根据频率选取随机的url
def get_random_url(data_dict):
    start = 0
    prob = data_dict.values()
    randnum = random.randint(1, sum(prob))
    for k, v in data_dict.items():
        start += v
        if randnum <= start:
            return k


def gen_email_conent(row):
    return row


def str_to_stamp(str_date):
    format_date = '%a, %d %b %Y%H:%M'
    datetime_date = time.strptime(str_date, format_date)
    return time.mktime(datetime_date)

def format_duration(TDuration):
    du = TDuration[:-1].split(' ')  # eg:从'Flight duration: 2h 25m'中获取['2h', '25m']
    mm = None
    hh = None
    for i in du: #
        if i[-1] == 'm':
            mm = i[:-1].rjust(2,'0')
        else:
            hh = i[:-1].rjust(2,'0')
    mm = '00' if mm == None else mm
    hh = '00' if hh == None else hh
    return hh + ':' + mm

def dateIsInvalid(dt): #判断该日期是否过期
    dt_time = time.strptime(dt, '%d/%m/%Y')
    dt_stamp = time.mktime(dt_time)
    if dt_stamp < time.time():
        return True
    return False

def format_seg_time(time_stamp):
    ti_tuple = time.localtime(time_stamp)
    ti_str = time.strftime('%Y-%m-%d %H:%M:%S', ti_tuple)
    return ti_str

def adjustDate(fromDate, num): #调整日期为今天之后，传入日期到第num天之前
    from_datetime = datetime.strptime(fromDate, '%d/%m/%Y')
    from_time = from_datetime.timetuple()
    from_stamp = time.mktime(from_time)
    diff = 0
    right_datetime = from_datetime
    while from_stamp < time.time():
        diff += 1
        if diff > num:
            return
        right_datetime = from_datetime + timedelta(days=diff)
        right_time = right_datetime.timetuple()
        from_stamp = time.mktime(right_time)
    final = right_datetime.strftime('%d/%m/%Y')
    return final

def str_date_format(str_date):
    date_datetime = datetime.strptime(str_date, '%a, %d %b %Y%H:%M')
    return date_datetime.strftime('%Y-%m-%d %H:%M:%S')

def get_port_city():
    try:
        res = requests.get(settings.GET_PORT_CITY_URL)
        jsonContent = json.loads(res.text)
        return jsonContent.get('data')
    except Exception as e:
        print(e)
        logging.info('get port city error')

if __name__ == '__main__':
    static = {}
    while True:
        url = get_random_url(settings.PUSH_DATA_URL)
        if url not in static:
            static[url] = 1
        else:
            static[url] += 1
        print(url)
        if sum(static.values()) >= 1000:
            break
    print(static)