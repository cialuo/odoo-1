# -*- coding:utf-8 -*-

import datetime

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def adjustDateTime2ZhCn(datatimsstr):
    """
    把基于utd的时间字符串校正到北京时间
    """
    t = datetime.datetime.strptime(datatimsstr, TIMEFORMAT)
    t = t + datetime.timedelta(hours=8)
    return t.strftime(TIMEFORMAT)
