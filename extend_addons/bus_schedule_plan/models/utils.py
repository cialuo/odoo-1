# -*- coding:utf-8 -*-

import datetime
import requests
import json

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

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
    if response.status_code != '200':
        return None
    try:
        return json.loads(response.text, encoding='utf-8')
    except Exception:
        return None
