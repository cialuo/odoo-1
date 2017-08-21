# -*-coding:UTF-8-*-

import requests
import datetime
import json
from requests import ConnectionError
import threading
import logging

logger = logging.getLogger('restful api')

class Client:

    '''restful客户端'''

    def __init__(self):

        #重试次数
        self.retry = 4

        #超时时间
        self.timeout = 5

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

        return False

    def http_post(self,url,**kwargs):

        '''
            发送post请求
        '''

        for i in range(self.retry):

            kwargs["timeout"] = self.timeout

            try:
                logger.info(u"第%s次发送请求===>url：%s ,参数：%s" % ((i+1),url,kwargs))
                response = requests.post(url, **kwargs)
                res = response.json()['resultMsg']
                logger.info(u"接受响应===>状态：%s，", res)
                return response

            except ConnectionError , e:

                logger.info(u'网络异常:%s' % (e.message))

                return False
            except Exception, e:

                if i >= self.retry - 1:

                    logger.info(u'restful 异常:%s' % (e.message))

                continue

        return False

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


'''互斥锁的声明'''
mutex_lock = threading.RLock()

class clientThread(threading.Thread):

    '''客户端线程'''


    def __init__(self, url,params,obj):
        threading.Thread.__init__(self)  # 线程类必须的初始化
        self.url = url  # 将传递过来的name构造到类中的name
        self.params = params
        self.obj = obj

    def run(self):

        global mutex_lock

        mutex_lock.acquire();  # 临界区开始，互斥的开始
        try:
            rp = Client().http_post(self.url, data=self.params)

            #服务器响应
            if rp:
                status_code = rp.status_code
                print '请求响应状态码:%s' % (rp.status_code)
                if status_code == 200:
                    print '数据推送：%s' % (self.params['params'])
                    print '请求响应JSON:%s' % (rp.json())
                    print self.obj
                else:
                    print '请检查参数或其他原因...'
        except Exception,e:
            print '推送数据异常:%s' % (e.message)
            logger.info('推送数据异常:%s' % (e.message))
        mutex_lock.release();  # python
        #print "%s被销毁了！" % (self.thread_name);res.write({'station_route_ids': [(6, 0, res_ids.ids)]})



