# -*-coding:UTF-8-*-

import requests
import datetime
import json
from requests import ConnectionError

class Client:

    '''restful客户端'''

    def __init__(self):

        #重试次数
        self.retry = 3

        #超时时间
        self.timeout = 25

        #响应正确编码
        self.status_code = 200

        #操作状态标志
        self.success_mark = 0


    def http_get(self,url,**kwargs):

        '''发送get请求'''

        for i in range(self.retry):

            kwargs["timeout"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:

                response = requests.get(url, **kwargs)

                # 如果返回正常,则取主键值
                if response.status_code == self.status_code and response.json()['result'] == self.success:
                    return response.json()['respose']['id']

            except ConnectionError , e:

                raise e

                break

            except Exception,e:

                if i >= self.retry -1:
                    raise e

                continue

        return ""
    def http_post(self,url,**kwargs):

        '''发送post请求'''

        for i in range(self.retry):

            kwargs["timeout"] = self.timeout

            try:

                response = requests.post(url, **kwargs)

                #如果返回正常,则取主键值
                if response.status_code == self.status_code and response.json()['result'] == self.success:

                    return response.json()['respose']['id']

            except ConnectionError , e:

                raise e

                break
            except Exception, e:

                if i >= self.retry - 1:
                    raise e

                continue

        return ""

class Params:

    '''参数类'''

    #1, 'SZ', 'op_line', vals
    def __init__(self,**kwargs):
        kwargs['editTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.params = self.get_params(**kwargs)

    def get_params(self,**kwargs):

        return json.dumps(kwargs)

    def to_dict(self):

        return self.__dict__
