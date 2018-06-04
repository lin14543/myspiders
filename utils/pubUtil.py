#encoding:utf-8
import sys
sys.path.append('..') # 测试专用
from myspiders import settings
import requests, json
from datetime import datetime, timedelta
import time, logging

BASIC_TIME = 0

def change_to_int(hms):
    h, m, s = hms.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def adjustDate(fromDate): #调整日期为今天之后
    from_datetime = datetime.strptime(fromDate, '%Y-%m-%d')
    from_time = from_datetime.timetuple()
    from_stamp = time.mktime(from_time)
    diff = 0
    right_datetime = from_datetime
    while from_stamp < time.time():
        diff += 1
        right_datetime = from_datetime + timedelta(days=diff)
        right_time = right_datetime.timetuple()
        from_stamp = time.mktime(right_time)
    final = right_datetime.strftime('%Y-%m-%d')
    return final

def dateIsInvalid(dt): # 是过去的日期
    dt_time = time.strptime(dt + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    dt_stamp = time.mktime(dt_time)
    if dt_stamp < time.time():
        return True
    return False

def analysisData(data):
    p = data.split(':')
    fromTo = p[0].split('-')
    dep = fromTo[0]
    to = fromTo[1]
    dt = datetime.strptime(p[1], '%Y%m%d').strftime('%Y-%m-%d')
    return (dt, dep, to)


def getUrl(carrier,num=1):
    params = {
        'carrier': carrier,
        'num': num,
    }
    try:
        content = requests.get(settings.GET_TASK_URL, params=params, timeout=settings.GET_URL_TIMEOUT).text
        s = requests.session()
        s.keep_alive = False
    except:
        return None
    data = json.loads(content)
    if 'status' not in data or data['status'] != 0:
        return None
    dt = data.get('data')
    return dt

def pushUrl(data):
    datas = {
        'carrier': data['carrier'],
        'als': data['als'],
        'dts': data['dts'],
    }
    try:
        res = requests.post(settings.PUSH_TASK_URL, data=json.dumps(datas), timeout=settings.GET_URL_TIMEOUT)
        s = requests.session()
        s.keep_alive = False
    except:
        logging.info('pushUrl Error...')

def invalidData(action, infos, push_data_url, host_name):
    if not len(infos):
        return True
    data = {
        'action': action,
        'data': infos,
        'name': host_name
    }
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        res = requests.post(push_data_url, data=json.dumps(data), headers={'Connection': 'close'}, timeout=settings.GET_URL_TIMEOUT)
        print('pushData: ' + res.text + ' num: ' + str(len(infos)))
        return True
    except:
        return False

def addData(action, infos, push_data_url, host_name):
    if not len(infos):
        return True
    data = {
        'action': action,
        'data': infos,
        'name': host_name
    }
    params = {'carrier': infos[0].get('carrier')}
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        res = requests.post(push_data_url, params=params, data=json.dumps(data), headers={'Connection': 'close'}, timeout=settings.GET_URL_TIMEOUT)
        print('pushData: ' + res.text + ' num: ' + str(len(infos)))
        return True
    except:
        return False

def insertLog(carrier, dt, dep, to, name, log_content):
    data = {}
    data['fromDate'] = time.mktime(time.strptime(dt, '%Y-%m-%d'))
    data['fromCity'] = dep
    data['toCity'] = to
    data['carrier'] = carrier
    data['content'] = log_content
    data['nodename'] = name
    datas = {
        'action' : 'add',
        'data': [data],
    }
    param = {'carrier': carrier}
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        res = requests.post(settings.LOG_URL, params=param, data=json.dumps(datas), timeout=settings.GET_URL_TIMEOUT)
    except:
        return

def heartbeat(name, carrier, num, permins):
    params = {
        'carrier': carrier,
        'num': num,
        'name': name,
        'permins': permins or 0
    }
    try:
        return requests.get(settings.HEARTBEAT_URL, params=params, timeout=settings.GET_URL_TIMEOUT).text
    except:
        return 'heartbeat error'

if __name__ == '__main__':
    task = {
        'arrAirport': 'BHX',
        'date': '20180615',
        'depAirport': 'VIE',
    }
    print(invalidData('invalid', [task], 'http://dx.spider2.jiaoan100.com/br/newairline?carrier=ew', 'lin'))
