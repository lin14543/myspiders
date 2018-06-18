#!/usr/bin/python
#coding:utf-8
import sys, requests, json, traceback, os, time
from dbUtil.db import DBHost
from myspiders import settings


def cpu_info():
    result = {}
    with open("/proc/cpuinfo", 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitline = line.split(":")
            keys = splitline[0].strip()
            if len(splitline) < 2:
                value = ''
            else:
                value = splitline[1].strip(' \t\n')
            result[keys] = value
    return result


def mem_info():
    result = {}
    with open("/proc/meminfo", 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitline = line.split(":")
            keys = splitline[0].strip()
            if len(splitline) < 2:
                value = ''
            else:
                value = splitline[1].strip(' \t\n')
            result[keys] = value
    return result


def handle_cmd(name):
    params = {'host': name}
    try:
        res = requests.get(settings.GET_CMD_URL, params=params, timeout=60)
        data_dict = json.loads(res.text)
    except:
        traceback.print_exc()
        return
    status = data_dict.get('status')
    if not status:
        cmds = data_dict.get('data')
        for cmd in cmds:
            print(cmd)
            os.system(cmd)


if __name__ == '__main__':
    host = sys.argv[1]
    db = DBHost()
    while True:
        cpu = cpu_info()
        mem = mem_info()
        handle_cmd(host)
        data = dict(
            host_name=host,
            model=cpu.get('model'),
            cpu_MHz=cpu.get('cpu MHz'),
            mem_free=mem.get('MemFree'),
            mem_available=mem.get('MemAvailable'),
            mem_total=mem.get('MemTotal'),
        )

        db.process_host(data)
        time.sleep(settings.MONITOR_DURATION)
