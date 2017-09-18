# -*- coding:utf-8 -*-

import datetime
import requests
import json
import re

timeFormatStr = "%Y-%m-%d %H:%M:%S"

def str2datetime(timestr):
    return datetime.datetime.strptime(timestr,timeFormatStr)

def timesubtraction(time1, time2):
    time1 = str2datetime(time1)
    time2 = str2datetime(time2)
    return round((time1 - time2).total_seconds()/3600.00,1)

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

mark_map = {
    1:'flat',
    2:'low',
    3:'peak'
}

def adjustDateTime2ZhCn(datatimsstr):
    """
    把基于utd的时间字符串校正到北京时间
    """
    t = datetime.datetime.strptime(datatimsstr, TIMEFORMAT)
    t = t + datetime.timedelta(hours=8)
    return t.strftime(TIMEFORMAT)


def getRuleFromBigData(url, citycode, lineId, curDate, reverseType):
    parms = {
        'city_code':citycode,
        'line_id':lineId,
        'cur_date':curDate,
        'reverse_type':reverseType
    }
    response = requests.get(url,params=parms)
    if response.status_code != 200:
        return None
    try:
        data = json.loads(response.text, encoding='utf-8')
    except Exception:
        return None

    if data['result'] != 0:
        return None
    data = data['response']
    vehicleup = []
    for item in data['planvehiclearrageup']:
        vehicleup.append((0,0,{
            'vehiclemode':item['vehiclemodel'],
            'workingnumber':item['workingnumber'],
            'backupnumber':item['backupnumber'],
        }))
    timeup = []
    for index, item in enumerate(data['timearrageup'], 1):
        timeup.append((0,0,{
            'starttime':item['starttime'],
            'seqid':index,
            'endtime':item['endtime'],
            'interval':item['ainterval'],
            'speed':item['speed'],
            'worktimelength':item['worktimelength'],
            'resttime':item['resttime'],
            'minvehicles':item['minvehicles'],
            'mark': mark_map[item['mark']],
            'spanday':True if item['spanday']==1 else False
        }))
    vehicledown = []
    timedown = []
    if reverseType == 'dubleway':
        for item in data['planvehiclearragedown']:
            vehicledown.append((0, 0, {
                'vehiclemode': item['vehiclemodel'],
                'workingnumber': item['workingnumber'],
                'backupnumber': item['backupnumber'],
            }))
        for index, item in enumerate(data['timearragedwon'], 1) :
            timedown.append((0, 0, {
                'starttime': item['starttime'],
                'seqid': index,
                'endtime': item['endtime'],
                'interval': item['interval'],
                'speed': item['speed'],
                'worktimelength': item['worktimelength'],
                'resttime': item['resttime'],
                'minvehicles': item['minvehicles'],
                'mark': mark_map[item['mark']],
                'spanday': True if item['spanday']==1 else False
            }))
    result = {
        'vup': vehicleup,
        'tup': timeup,
        'vdown': vehicledown,
        'tdown': timedown
    }
    return result



def check_time_format(time):
    """
    检查时间格式是否正确
    :param time: 09:00
    :return: False/True
    """
    reg = '^(0\d{1}|1\d{1}|2[0-3]):([0-5]\d{1})$'
    return re.match(reg, time)