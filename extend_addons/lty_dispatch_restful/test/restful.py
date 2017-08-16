# -*-coding:UTF-8-*-

import requests
import json

from requests import ConnectionError


def post():
    url = 'http://10.1.50.83:8080/ltyop/syn/synData/'

    jsonData = {
    "type": "2",
    "cityCode": "SZ",
    "editTime": "2017:08:09 19:34:50",
    "tableName": "op_line",
    "data": "{'keyWord':'333','lineName':'宝深路','id':'2113'}"
    }

    params = json.dumps(jsonData)

    data = {
        "params":params
    }


    #try:


    print data

    rp = requests.post(url,data=data)

    print rp.url
    #rp = requests.get(url,params=jsonData)
    #rp = requests.post(url)
    print rp.status_code
    print rp.text
    print rp.json()['respose']['id']
    #except ConnectionError:
    #print '接口链接异常，前检查网络....'



if __name__ == '__main__':
    post()